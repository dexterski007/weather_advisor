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
    with app.app_context():
        create_indexes()

    from .routes import main
    app.register_blueprint(main)

    return app

def create_indexes():
    """Create necessary indexes for the MongoDB collection"""
    try:
        mongo.db.activities.create_index([
            ("weather_conditions.sunny.outdoor_activities", "text"),
            ("weather_conditions.sunny.indoor_activities", "text"),
            ("weather_conditions.rainy.outdoor_activities", "text"),
            ("weather_conditions.rainy.indoor_activities", "text"),
            ("weather_conditions.snowy.outdoor_activities", "text"),
            ("weather_conditions.snowy.indoor_activities", "text"),
            ("weather_conditions.windy.outdoor_activities", "text"),
            ("weather_conditions.windy.indoor_activities", "text"),
            ("weather_conditions.stormy.outdoor_activities", "text"),
            ("weather_conditions.stormy.indoor_activities", "text"),
            ("weather_conditions.cloudy.outdoor_activities", "text"),
            ("weather_conditions.cloudy.indoor_activities", "text")
        ])
        print("Indexes created successfully.")
    except Exception as e:
        print(f"Error creating indexes: {str(e)}")
