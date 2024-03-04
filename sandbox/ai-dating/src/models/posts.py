from datetime import datetime, timezone

from src.app import db
from src.models.base_model import BaseModel
from src.models.users import User


class Post(BaseModel):
    body = db.Column(db.Text())
    timestamp = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    
    user_id = db.Column(db.ForeignKey(User.id), index=True)
    author = db.relationship('User', back_populates='posts')
