FROM python:slim
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt


COPY migrations migrations
COPY src src

ENV FLASK_APP="src.app:create_app()"

EXPOSE 5001
CMD ["gunicorn", "-b", "localhost:8001", "src.app:create_app()"]