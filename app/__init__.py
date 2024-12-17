from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .config import config_by_name


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name="production"):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from .posts.models import Post
        from . import views
        from .posts import posts_blueprint
        from .users import users_blueprint
        app.register_blueprint(posts_blueprint)
        app.register_blueprint(users_blueprint)

    return app