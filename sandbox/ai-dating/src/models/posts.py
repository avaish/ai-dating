
from datetime import datetime, timezone
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, Text
from sqlalchemy.orm import Session, sessionmaker
from typing import Iterator, Optional

from src.lib.db_utils import get_engine
from src.models.base_model import BaseDBModel
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

class PostRepository:
    def save(self, post: Post):
        raise NotImplementedError()

    def get_by_id(self, id: int) -> Optional[Post]:
        raise NotImplementedError()

class SQLPostRepository(PostRepository):
    def __init__(self, session: Session):
        self._session: Session = session

    def save(self, post: Post):
        self._session.add(PostDB(id=post.id, user_id=post.user_id, body=post.body))

    def get_by_id(self, id: int) -> Optional[Post]:
        instance = self._session.query(PostDB).filter(PostDB.id == id).first()

        if instance:
            return Post(id=instance.id, user_id=instance.user_id, body=instance.body)

def create_post_repository() -> Iterator[PostRepository]:
    session = sessionmaker(bind=get_engine())()
    post_repository = SQLPostRepository(session)

    try:
        yield post_repository
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
