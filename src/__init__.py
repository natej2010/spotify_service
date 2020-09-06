from flask import Flask
from instance.config import app_config

import os

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)

    app.secret_key = bytes(os.getenv('SECRET'), 'utf-8')

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    # Import Blueprints
    from .api.spotify import spotify

    # Register Blueprints
    app.register_blueprint(spotify)

    return app
