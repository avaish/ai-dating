from datetime import datetime, timezone
from typing import Any, TypeVar

from src.app import db

import sqlalchemy as sa
import sqlalchemy.orm as so

T = TypeVar("T", bound="BaseModel")

class BaseModel(db.Model):
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
