import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = True
    TESTING = False
    OPEN_API_KEY = os.environ.get("OPENAI_API_KEY", "secret-key")
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://ai_dating:ai_dating@db:5432/ai_dating_dev')

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
