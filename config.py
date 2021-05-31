import os
from datetime import timedelta


class Config:
    HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    DEBUG = int(os.getenv("FLASK_DEBUG", "1"))
    PORT = int(os.getenv("FLASK_PORT", "5000"))
    TESTING = False
    CSRF_ENABLED = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True


class Productionconfig(Config):
    DEBUG = False


app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": Productionconfig,
}
