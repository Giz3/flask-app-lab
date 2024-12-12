import os
from dotenv import load_dotenv


load_dotenv()

def get(variable_name: str, variable_type: type = str):
    """Отримує значення змінної середовища та перетворює її у вказаний тип."""
    value = os.getenv(variable_name)
    if value is None:
        return None
    try:
        return variable_type(value)
    except ValueError:
        return None


class Config:
    """Базова конфігурація для Flask додатку."""
    SECRET_KEY = get("SECRET_KEY", str) or "default_secret_key"
    FLASK_DEBUG = get("FLASK_DEBUG", bool) or False


class DevelopmentConfig(Config):
    """Конфігурація для розвитку."""
    FLASK_DEBUG = True
    ENV = "development"


class ProductionConfig(Config):
    """Конфігурація для продуктивного середовища."""
    FLASK_DEBUG = False
    ENV = "production"


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}