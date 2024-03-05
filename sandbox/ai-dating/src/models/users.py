from pydantic import BaseModel
from sqlalchemy import Column, String
from typing import Iterator, Optional, Self

from src.models.base_model import BaseDBModel, Repository, create_repository

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

    def to_db(self) -> UserDB:
        UserDB(id=self.id, username=self.username, email=self.email, password_hash=self.password_hash)

    @staticmethod
    def from_db(user_db: UserDB) -> Self:
        return User(id=user_db.id, username=user_db.username, email=user_db.email, password_hash=user_db.password_hash)


def create_user_repository() -> Repository[User]:
    return next(create_repository(User, UserDB))
