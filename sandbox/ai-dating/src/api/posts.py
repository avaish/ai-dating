from flask import Blueprint

from src.lib.utils import request_fields
from src.models.posts import Post

posts_bp = Blueprint("posts", __name__)

@posts_bp.route("/v1/posts", methods=["GET"])
def get_posts():
    posts = Post.list()
    resp = []
    for post in posts:
        resp.append(post.to_dict())
    return resp

@posts_bp.route("/v1/posts/<post_id>", methods=["GET"])
def get_post(post_id: str):
    return Post.get(post_id).to_dict()

@posts_bp.route("/v1/posts", methods=["POST"])
@request_fields({"input"})
def create_post(input: str):
    post = Post(body=input, user_id=1)
    post.save()
    return post.to_dict()
