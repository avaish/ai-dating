
from datetime import datetime, timezone
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, Text
from typing import Iterator

from src.models.base_model import BaseDBModel, Repository, create_repository
from src.models.users import UserDB

from sqlalchemy.ext.declarative import declarative_base

PostBase = declarative_base()

class PostDB(PostBase, BaseDBModel):
    __tablename__ = "posts"

    body = Column(Text())
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    user_id = Column(ForeignKey(UserDB.id), index=True)

class Post(BaseModel):
    id: int
    user_id: int
    body: str

def create_post_repository() -> Repository[Post]:
    return next(create_repository(Post, PostDB))
