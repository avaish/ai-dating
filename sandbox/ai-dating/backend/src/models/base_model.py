from datetime import datetime
from typing import Generic, Iterator, Optional, TypeVar
import uuid


from sqlalchemy import Column, DateTime, Integer, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session, sessionmaker

from src.lib.db_utils import get_engine

T = TypeVar("T")
V = TypeVar('V')



class BaseDBModel():
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)

class Repository(Generic[T]):
    def save(self, object: T):
        raise NotImplementedError()

    def get_by_id(self, id: str) -> Optional[T]:
        raise NotImplementedError()

    def get_by_filter(self) -> list[T]:
        raise NotImplementedError()

    def list(self) -> list[T]:
        raise NotImplementedError()

class SqlRepository(Repository[T]):
    def __init__(self, session: Session, obj_class: type[T], db_class: type[V]):
        self._session: Session = session
        self.obj_class: type[T] = obj_class
        self.db_class: type[V] = db_class

    def save(self, object: T):
        curr_time = datetime.now()
        object.created_at = object.created_at or curr_time
        object.updated_at = curr_time

        self._session.add(object.to_db())
        self._session.commit()

    def get_by_id(self, id: str) -> Optional[T]:
        instance = self._session.query(self.db_class).filter(self.db_class.id == id).first()

        if instance:
            return self.obj_class.from_db(instance)
        return None

    def get_by_filter(self) -> list[T]:
        # TODO: Implement this
        pass

    def list(self) -> list[T]:
        instances = self._session.scalars(select(self.db_class)).all()
        objects = []
        for instance in instances:
            objects.append(self.obj_class.from_db(instance))
        return objects

def create_repository(cls1: type[T], cls2: type[V]) -> Iterator[Repository[T]]:
    session = sessionmaker(bind=get_engine())()
    repository = SqlRepository[cls1](session, cls1, cls2)

    try:
        yield repository
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
