from flask import Blueprint

posts_bp = Blueprint("posts", __name__)

@posts_bp.route("/v1/posts", methods=["GET"])
def get_posts():
    return "Got Posts"

@posts_bp.route("/v1/posts/<post_id>", methods=["GET"])
def get_post(post_id: str):
    return post_id
