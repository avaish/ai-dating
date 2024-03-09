import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = True
    TESTING = False

    DB_USER=os.environ("DB_USER")
    DB_PASSWORD=os.environ("DB_PASSWORD")
    DB_HOST=os.environ("DB_HOST")
    DB_PORT=os.environ("DB_PORT")
    DB_NAME=os.environ("DB_NAME")
    OPEN_API_KEY = os.environ.get("OPENAI_API_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

class ProductionConfig(Config):
    FLASK_DEBUG = False

class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

def get_config():
    return DevConfig()
