#!/bin/sh

# flask db migrate -m "Create tables"
gunicorn --bind 0.0.0.0:8001 --workers 4 "src.app:create_app()"

exec "$@"