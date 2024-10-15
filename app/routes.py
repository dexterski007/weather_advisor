from flask import Blueprint, request, jsonify, current_app
import random
from .services import get_weather_data, suggest_activity, get_weather_forecast, get_activity_list
from .models import get_coordinates
from . import mongo

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def welcome():
    return jsonify({"message": "Welcome to the Weather Advisor API!"})

@main.route('/recommend', methods=['GET'])
def recommend_activity():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    weather_data = get_weather_data(city)

    if 'error' in weather_data:
        return jsonify(weather_data), 400

    activity = suggest_activity(weather_data)

    return jsonify({
        "activity": activity
    })

@main.route('/weather/forecast', methods=['GET'])
def get_forecast():
    city = request.args.get('city')
    days = request.args.get('days', 3)
    if not city:
        return jsonify({"error": "city parameter is required."}), 400

    result = get_weather_forecast(city, days)
    if result.get('error'):
        return jsonify(result), 400
    return jsonify(result)

@main.route('/activities', methods=['GET'])
def get_activities():
    weather = request.args.get('weather', None)
    activity_type = request.args.get('type', 'outdoor')
    limit = request.args.get('limit', 5)

    result = get_activity_list(weather, activity_type, limit)
    if result.get('error'):
        return jsonify(result), 400
    return jsonify(result)

@main.route('/activities/random', methods=['GET'])
def get_random_activity():
    weather = request.args.get('weather', None)
    activity_type = request.args.get('type', 'outdoor')
    limit = request.args.get('limit', 10)

    result = get_activity_list(weather, activity_type, limit)
    if result.get('error'):
        return jsonify(result), 400

    choice = random.choice(result['activities'])
    return jsonify({
        "activity": choice
    })

@main.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    weather_data = get_weather_data(city)

    if 'error' in weather_data:
        return jsonify(weather_data), 400

    return jsonify(weather_data)

@main.route('/activities/search', methods=['GET'])
def activity_search():
    activity = request.args.get('activity')
    type = request.args.get('type')
    if not activity:
        return jsonify({"error": "Activity parameter is required"}), 400

    result = get_activity_list(activity, type, 10)
    if result.get('error'):
        return jsonify(result), 400

    return jsonify(result)

@main.route('/geocoding', methods=['GET'])
def geocoding():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    result = get_coordinates(city)
    if result.get('error'):
        return jsonify(result), 400
    return jsonify(result)

@main.route('/activities', methods=['POST'])
def add_activity():
    try:
        new_activity = request.get_json()

        weather = new_activity.get('weather')
        activity_type = new_activity.get('type')
        activity_name = new_activity.get('activity')

        if not all([weather, activity_type, activity_name]):
            return jsonify({"error": "Missing weather, type, or activity field."}), 400

        mongo.db.user_activities.update_one(
            {'weather': weather},
            {
                '$setOnInsert': {
                    'outdoor_activities': [],
                    'indoor_activities': []
                },
                '$addToSet': {f"{activity_type}_activities": activity_name}
            },
            upsert=True
        )

        return jsonify({"message": "User activity added successfully!"}), 201

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

