from flask import Blueprint

from src.lib.utils import request_fields
from src.models.users import User

users_bp = Blueprint("users", __name__)

@users_bp.route("/v1/users", methods=["GET"])
def get_users():
    users = User.list()
    resp = []
    for user in users:
        resp.append(user.to_dict())
    return resp

@users_bp.route("/v1/users/<id>", methods=["GET"])
def get_user(id: str) -> User:
    return User.get(id).to_dict()

@users_bp.route("/v1/users", methods=["POST"])
@request_fields({"username", "email"})
def create_user(username: str, email: str) -> User:
    user = User(username=username, email=email)
    user.save()
    return user.to_dict()

