from typing import Generic, Iterator, Mapping, Optional, TypeVar


from sqlalchemy import Column, DateTime, Integer, select
from sqlalchemy.orm import Session, sessionmaker

from src.lib.db_utils import get_engine

T = TypeVar("T")
V = TypeVar('V')

class BaseDBModel():
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)

class Repository(Generic[T]):
    def save(self, object: T):
        raise NotImplementedError()

    def get_by_id(self, id: int) -> Optional[T]:
        raise NotImplementedError()

    def list(self) -> list[T]:
        raise NotImplementedError()

class SqlRepository(Repository[T]):
    def __init__(self, session: Session, obj_class: type[T], db_class: type[V]):
        self._session: Session = session
        self.obj_class: type[T] = obj_class
        self.db_class: type[V] = db_class

    def save(self, object: T):
        self._session.add(object.to_db())

    def get_by_id(self, id: int) -> Optional[T]:
        instance = self._session.query(self.db_class).filter(self.db_class.id == id).first()

        if instance:
            return T.from_db(instance)

    def list(self) -> list[T]:
        instances = self._session.scalars(select(self.db_class)).all()
        users = []
        for instance in instances:
            users.append(self.obj_class.from_db(instance))
        return users

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
