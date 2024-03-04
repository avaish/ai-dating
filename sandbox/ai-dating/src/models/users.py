from src.app import db
from src.models.base_model import BaseModel


class User(BaseModel):
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(256))
    posts = db.relationship('Post', back_populates='author')
