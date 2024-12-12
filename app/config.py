from utils.config import get


class BaseConfig:
    SECRET_KEY = get("SECRET_KEY") or "default_secret_key"
    FLASK_DEBUG = bool(get("FLASK_DEBUG")) or False


class DevelopmentConfig(BaseConfig):
    FLASK_DEBUG = True
    ENV = "development"


class ProductionConfig(BaseConfig):
    FLASK_DEBUG = False
    ENV = "production"


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}