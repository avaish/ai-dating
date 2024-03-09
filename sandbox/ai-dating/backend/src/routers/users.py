from fastapi import APIRouter, Depends

from src.models.base_model import Repository
from src.models.users import User, create_user_repository

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_users(user_repository: Repository[User] = Depends(create_user_repository)):
    return user_repository.list()


@router.get("/me")
async def read_user_me(user_repository: Repository[User] = Depends(create_user_repository)):
    user_repository.save(User.create(username="sworls1", email="abcd@def", password_hash="abc"))
    return {"username": "1111"}


@router.get("/{username}")
async def read_user(username: str):
    return {"username": username}
