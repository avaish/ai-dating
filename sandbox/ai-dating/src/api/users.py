from flask import Blueprint

users_bp = Blueprint("users", __name__)

@users_bp.route("/v1/users", methods=["GET"])
def get_posts():
    return "Got Users"

@users_bp.route("/v1/users/<user_id>", methods=["GET"])
def get_post(user_id: str):
    return user_id