from flask import Flask
from .config import config_by_name


def initialize_app(config_type="production"):
    app = Flask(__name__)
    
    app.config.from_object(config_by_name.get(config_type, config_by_name["production"]))

    with app.app_context():

        from . import views
        from .posts import posts_blueprint
        from .users import users_blueprint
        
        app.register_blueprint(posts_blueprint)
        app.register_blueprint(users_blueprint)

    return app