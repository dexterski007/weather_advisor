from flask import Flask
from flask_caching import Cache
from flask_pymongo import PyMongo  # Import PyMongo
from config import Config

cache = Cache()
mongo = PyMongo()  # Initialize the PyMongo instance

def create_app():
    '''Creates a Flask app instance'''
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the cache
    cache.init_app(app)

    # Initialize MongoDB
    mongo.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app
