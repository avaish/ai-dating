from flask import Blueprint

from src.lib.utils import request_fields
from src.models.posts import Post

posts_bp = Blueprint("posts", __name__)

@posts_bp.route("/v1/posts", methods=["GET"])
def get_posts():
    return "Got Posts"

@posts_bp.route("/v1/posts/<post_id>", methods=["GET"])
def get_post(post_id: str):
    return post_id

@posts_bp.route("/v1/posts", methods=["POST"])
@request_fields({"input"})
def create_post(input: str):
    Post()
