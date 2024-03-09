#!/bin/sh

uvicorn src.main:app --proxy-headers --host 0.0.0.0 --port 8001 --reload

# alembic init migrations
# alembic revision --autogenerate -m "Create a baseline migrations"
# alembic upgrade head

exec "$@"
