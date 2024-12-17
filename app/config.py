from utils.config import get


class Config:
    SECRET_KEY = get("SECRET_KEY") or "default_secret_key"
    FLASK_DEBUG = bool(get("FLASK_DEBUG")) or False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    FLASK_DEBUG = True
    ENV = "development"


class ProductionConfig(Config):
    FLASK_DEBUG = False
    ENV = "production"


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}