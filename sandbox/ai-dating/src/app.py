from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
import sys

from src.config import DevConfig

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

db = SQLAlchemy()
migrate = Migrate()

def register_routes(app: Flask):
    from src.api.health import health_bp
    from src.api.posts import posts_bp
    from src.api.users import users_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(users_bp)

def create_app(config_class=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    db.init_app(app)
    migrate.init_app(app, db)

    if not app.debug and not app.testing:
        pass

    register_routes(app)

    from src.models.posts import Post
    from src.models.users import User

    return app
