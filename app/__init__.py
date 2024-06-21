from flask import Flask
from config.config import Config
from logging_config import setup_logging

setup_logging()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        from . import routes

    return app
