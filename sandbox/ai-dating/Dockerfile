FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/src"

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt


COPY migrations migrations
COPY src src