import functools
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from src.config import get_config

config = get_config()

DB_URL = URL.create(
    drivername="postgresql",
    username=config.DB_USER,
    password=config.DB_PASSWORD,
    host=config.DB_HOST,
    database=config.DB_NAME,
    port=config.DB_PORT
)

@functools.lru_cache(maxsize=None)
def get_engine():
    return create_engine(DB_URL, pool_pre_ping=True)

def get_db_url():
    return DB_URL
