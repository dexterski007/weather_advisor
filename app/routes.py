from flask import Blueprint, request, jsonify, current_app
import requests
from .services import get_weather_data, suggest_activity, get_weather_forecast, get_activity_list
import random

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

    result = (get_weather_forecast(city, days))
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
