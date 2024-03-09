from fastapi import APIRouter, Depends, HTTPException
from langchain_core.prompts import ChatPromptTemplate
import os

from src.models.posts import Post, create_post_repository
from src.models.users import User, create_user_repository
from src.lib.open_api_client import get_open_api_client, create_human_message
from src.lib.prompts import PROFILE_GURU_PROMPT

from src.models.base_model import Repository

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)

fake_posts_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}

IMAGE_DIR = "/app/images"

@router.get("/")
async def read_posts(user_id: str="1dfc7961-7d6a-479a-8778-1925752e13d6", post_repository: Repository[Post] = Depends(create_post_repository), user_repository: Repository[User] = Depends(create_user_repository)):
    user = user_repository.get_by_id(user_id)
    open_api_client = get_open_api_client()

    images = []
    for _, _, filenames in os.walk(IMAGE_DIR):
        images = filenames


    human_message = create_human_message(images)
    PROFILE_GURU_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([("system", PROFILE_GURU_PROMPT), human_message])
    chain = PROFILE_GURU_PROMPT_TEMPLATE | open_api_client.chat_model
    result = chain.invoke({})
    print(type(result), result)
    # post = Post.create(user_id=user.id, body=result)
    # post_repository.save(post)

    return post_repository.list()

    # return fake_posts_db


@router.get("/{post_id}")
async def read_post(post_id: str):
    if post_id not in fake_posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"name": fake_posts_db[post_id]["name"], "post_id": post_id}


@router.put(
    "/{post_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_post(post_id: str, post_repository: Repository[Post] = Depends(create_post_repository)):
    if post_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": post_id, "name": "The great Plumbus"}
