from fastapi import FastAPI
import logging
from logging.config import dictConfig

from src.internal import admin
from src.routers import chats, posts, users
from src.lib.logging import LogConfig
from src.lib.db_utils import get_db_url

# Set-up logging
dictConfig(LogConfig().dict())
logger = logging.getLogger("ai-dating")

# Configure FastAPI
app = FastAPI()

app.include_router(admin.router)
app.include_router(chats.router)
app.include_router(users.router)
app.include_router(posts.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
