from fastapi import APIRouter, Depends, HTTPException


from src.models.base_model import Repository
from src.models.posts import Post, create_post_repository


router = APIRouter(
    prefix="/api/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)

fake_posts_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}

@router.get("/")
async def read_posts(post_repository: Repository[Post] = Depends(create_post_repository)):
    return post_repository.list()


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
