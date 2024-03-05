from pydantic import BaseModel
from sqlalchemy import Column, String, select
from sqlalchemy.orm import Session, sessionmaker
from typing import Iterator, Optional

from src.lib.db_utils import get_engine
from src.models.base_model import BaseDBModel

from sqlalchemy.ext.declarative import declarative_base

UserBase = declarative_base()

class UserDB(UserBase, BaseDBModel):
    __tablename__ = "users"

    username = Column(String(64), unique=True, index=True)
    email = Column(String(120), unique=True, index=True)
    password_hash = Column(String(256))

class User(BaseModel):
    id: int
    username: str
    email: str
    password_hash: Optional[str] = None

class UserRepository:
    def save(self, user: User):
        raise NotImplementedError()

    def get_by_id(self, id: int) -> Optional[User]:
        raise NotImplementedError()

    def list(self) -> list[User]:
        raise NotImplementedError()

class SQLUserRepository(UserRepository):
    def __init__(self, session: Session):
        self._session: Session = session

    def save(self, user: User):
        self._session.add(UserDB(id=user.id, username=user.username, email=user.email, password_hash=user.password_hash))

    def get_by_id(self, id: int) -> Optional[User]:
        instance = self._session.query(UserDB).filter(UserDB.id == id).first()

        if instance:
            return User(id=instance.id, username=instance.username, email=instance.email)

    def list(self) -> list[User]:
        instances = self._session.scalars(select(UserDB)).all()
        users = []
        for instance in instances:
            users.append(User(id=instance.id, username=instance.username, email=instance.email))
        return users

def create_user_repository() -> Iterator[UserRepository]:
    session = sessionmaker(bind=get_engine())()
    user_repository = SQLUserRepository(session)

    try:
        yield user_repository
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
