import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = "postgresql://ai_dating:ai_dating@db:5432/ai_dating_dev"
    
class ProductionConfig(Config):
    DEBUG = False

class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


