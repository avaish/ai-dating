
from datetime import datetime, timezone
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, Text
from typing import Optional, Self
import uuid

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
    id: uuid.UUID
    user_id: uuid.UUID
    body: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_db(self) -> PostDB:
        return PostDB(
            id=self.id,
            user_id=self.user_id,
            body=self.body,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @staticmethod
    def create(user_id: str, body: str) -> Self:
        id_ = uuid.uuid4()
        return Post(id=id_, user_id=user_id, body=body)

    @staticmethod
    def from_db(post_db: PostDB) -> Self:
        return Post(
            id=post_db.id,
            user_id=post_db.user_id,
            body=post_db.body,
            created_at=post_db.created_at,
            updated_at=post_db.updated_at
        )

def create_post_repository() -> Repository[Post]:
    return next(create_repository(Post, PostDB))
