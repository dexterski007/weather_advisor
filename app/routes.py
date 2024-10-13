from flask import Blueprint, request, jsonify
from .services import get_weather_data, suggest_activity

main = Blueprint('main', __name__)

@main.route('/recommend', methods=['GET'])
def recommend_activity():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    # Fetch weather data
    weather_data = get_weather_data(city)
    
    if 'error' in weather_data:
        return jsonify(weather_data), 400

    # Recommend an activity based on weather
    activity = suggest_activity(weather_data)
    
    return jsonify({
        "city": city,
        "activity": activity,
        "weather": weather_data
    })
