# pull official base image
FROM python:3.11.3-slim-buster

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/src"

# install system dependencies
RUN apt-get update && apt-get install -y netcat libpq-dev

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy project
COPY images images
COPY migrations migrations
COPY src src
COPY entrypoint.sh entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
