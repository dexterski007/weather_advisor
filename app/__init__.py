from flask import Flask
from flask_caching import Cache
from config import Config

cache = Cache()


def create_app():
    '''Creates a Flask app instance'''
    app = Flask(__name__)
    app.config.from_object(Config)

    from .routes import main
    app.register_blueprint(main)

    return app
