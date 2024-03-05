import functools
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

DB_URL = URL.create(
    drivername="postgresql",
    username="ai_dating",
    password="ai_dating",
    host="db",
    database="ai_dating_dev",
    port=5432
)

@functools.lru_cache(maxsize=None)
def get_engine():
    return create_engine(DB_URL, pool_pre_ping=True)

def get_db_url():
    return DB_URL
