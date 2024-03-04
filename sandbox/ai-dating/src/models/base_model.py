from datetime import datetime, timezone
from typing import Any, TypeVar

from src.app import db

import sqlalchemy as sa
import sqlalchemy.orm as so

T = TypeVar("T", bound="BaseModel")

class DefaultRepr:
    """Mixin that overrides __repr__ with an object's class' name and its internal state.

    e.g., "MyDefaultRepr('dict_': {'b': ['c', 'd']}, 'number': 3, 'string': 'a')"
    """

    def __repr__(self) -> str:
        key_value_pairs = [f"{key}={value!r}" for key, value in self.__dict__.items()]
        key_value_str = ", ".join(key_value_pairs)
        return f"{self.__class__.__name__}({key_value_str})"

class BaseModel(db.Model, DefaultRepr):
    __abstract__ = True
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False)

    @classmethod
    def get(cls: type[T], id: int) -> T:
        return db.session.query(cls).filter(cls.id == id).first()

    @classmethod
    def list(cls: type[T]) -> list[T]:
        return db.session.scalars(sa.select(cls)).all()
    
    def to_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def before_save(self, *args, **kwargs):
        current_time = datetime.now(timezone.utc)
        if not self.created_at:
            self.created_at = current_time
        self.updated_at = current_time

    def after_save(self, *args, **kwargs):
        pass

    def save(self, commit=True):
        self.before_save()
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e

        self.after_save()

    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()
