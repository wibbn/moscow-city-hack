import os

from flask import Flask

from config import config

app = Flask(__name__, static_url_path='')
app.config["DEBUG"] = True

def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .api.v1 import blueprint as api
    app.register_blueprint(api, url_prefix="/api/v1")

    return app

basedir = os.path.abspath(os.path.dirname(__file__))