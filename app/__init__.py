from flask import Flask
from flask_caching import Cache
from flask_pymongo import PyMongo
from config import Config

cache = Cache()
mongo = PyMongo()

def create_app():
    '''Creates a Flask app instance'''
    app = Flask(__name__)
    app.config.from_object(Config)

    cache.init_app(app)

    mongo.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app
