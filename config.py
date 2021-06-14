import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    YNDX_GEOCODE_TOKEN = os.environ.get('YNDX_GEOCODE_TOKEN')

    APP_NAME = os.environ.get("APP_NAME") or "bestplaces"
    APP_HOSTNAME = os.environ.get("APP_HOSTNAME") or "localhost:5000"

    @classmethod
    def init_app(cls, app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False

class HerokuConfig(ProductionConfig):
    SSL_REDIRECT = True if os.environ.get('DYNO') else False

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

config = {
    'development': DevelopmentConfig,
    "testing": TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    "heroku": HerokuConfig,
}