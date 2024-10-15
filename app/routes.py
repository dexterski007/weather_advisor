from flask import Blueprint, request, jsonify, current_app
import random
from .services import get_weather_data, suggest_activity, get_weather_forecast, get_activity_list, search_activities_in_db, add_activity_to_db, remove_activity_from_db, reindex_database
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
    activity_type = request.args.get('type', 'all')
    limit = request.args.get('limit', None)

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
    activity_query = request.args.get('activity')
    activity_type = request.args.get('type', None)  # Optional: outdoor, indoor, or all

    if not activity_query:
        return jsonify({"error": "Activity query parameter is required"}), 400

    search_result = search_activities_in_db(activity_query, activity_type)

    if not search_result:
        return jsonify({"error": "No matching activities found."}), 404

    return jsonify(search_result)

@main.route('/geocoding', methods=['GET'])
def geocoding():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    result = get_coordinates(city)
    if result.get('error'):
        return jsonify(result), 400
    return jsonify(result)

@main.route('/activities/add', methods=['POST'])
def add_activity():
    new_activity = request.json.get('activity')
    weather = request.json.get('weather')
    activity_type = request.json.get('type')

    if not new_activity or not weather or not activity_type:
        return jsonify({"error": "Missing required fields: activity, weather, type"}), 400

    result = add_activity_to_db(new_activity, weather, activity_type)
    
    if 'error' in result:
        return jsonify(result), 400

    reindex_database()

    return jsonify(result)

@main.route('/activities/remove', methods=['POST'])
def remove_activity():
    activity = request.json.get('activity')
    weather = request.json.get('weather')
    activity_type = request.json.get('type')

    if not activity or not weather or not activity_type:
        return jsonify({"error": "Missing required fields: activity, weather, type"}), 400

    result = remove_activity_from_db(activity, weather, activity_type)
    
    if 'error' in result:
        return jsonify(result), 400

    reindex_database()

    return jsonify(result)
