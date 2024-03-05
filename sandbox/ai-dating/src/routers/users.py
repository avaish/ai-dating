from fastapi import APIRouter, Depends

from src.models.users import User, UserRepository, create_user_repository

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_users(user_repository: UserRepository = Depends(create_user_repository)):
    return user_repository.list()


@router.get("/me")
async def read_user_me():
    return {"username": "1111"}


@router.get("/{username}")
async def read_user(username: str):
    return {"username": username}
