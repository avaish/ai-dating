from flask import Blueprint
from langchain.schema import HumanMessage, SystemMessage

from src.lib.open_api_client import create_message, get_open_api_client
from src.lib.prompts import PROFILE_GURU_PROMPT_TEMPLATE
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

@posts_bp.route("/v1/posts:chatGPT", methods=["GET"])
def create_gpt_post():
    open_api_client = get_open_api_client()

    prompt_value = PROFILE_GURU_PROMPT_TEMPLATE.invoke({})
    post = Post(body=prompt_value.to_string(), user_id=1)
    post.save()

    result = open_api_client.invoke(prompt_value)
    post = Post(body=result.content, user_id=1)
    post.save()

    human_message = create_message(HumanMessage, "Here is a photo")
    post = Post(body=human_message.content, user_id=1)
    post.save()

    # Checkpoint -- this is erroring
    result = open_api_client.invoke(human_message)
    post = Post(body=result.content, user_id=1)
    post.save()

    return post.to_dict()
