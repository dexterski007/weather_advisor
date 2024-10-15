import requests
from flask import current_app
import random
from app import cache, mongo
from .utils import get_combined_activities

@cache.cached(timeout=300, key_prefix='weather_data_{city}')
def get_weather_data(city):
    '''Fetches weather data from OpenWeatherMap API'''
    api_key = current_app.config['WEATHER_API_KEY']
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Unable to fetch weather data"}

    data = response.json()
    weather = {
        "description": data["weather"][0]["description"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"]
    }
    return weather

def map_weather_condition(description):
    '''Maps weather description to a weather condition'''
    if 'clear' in description or 'sun' in description:
        return 'sunny'
    elif 'rain' in description:
        return 'rainy'
    elif 'snow' in description:
        return 'snowy'
    elif 'wind' in description:
        return 'windy'
    elif 'storm' in description or 'thunderstorm' in description:
        return 'stormy'
    else:
        return 'cloudy'

def suggest_activity(weather_data):
    '''Suggests an activity based on the weather data'''
    description = weather_data['description']
    temp = weather_data['temperature']
    wind_speed = weather_data['wind_speed']

    condition = map_weather_condition(description)
    activities_json = get_activities_from_db(condition)

    if temp > 298 and 'water' in activities_json:
        activity_list = activities_json.get('outdoor_activities', [])
    elif temp < 283 or wind_speed > 10:
        activity_list = activities_json.get('indoor_activities', [])
    else:
        activity_list = activities_json.get('outdoor_activities', activities_json.get('indoor_activities', []))

    return random.choice(activity_list) if activity_list else None

@cache.cached(timeout=300, key_prefix='forecast_data_{city}')
def get_weather_forecast(city, days):
    '''Fetches weather forecast data from OpenWeatherMap API'''
    weather_api_key = current_app.config['WEATHER_API_KEY']
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&cnt={int(days)}&appid={weather_api_key}&units=metric"

    response = requests.get(forecast_url)

    if response.status_code != 200:
        return {"error": "Unable to fetch weather data."}

    forecast_data = response.json()

    forecast_list = []
    for forecast in forecast_data['list']:
        forecast_item = {
            "date": forecast['dt_txt'],
            "temperature": forecast['main']['temp'],
            "description": forecast['weather'][0]['description'],
            "humidity": forecast['main']['humidity'],
            "wind_speed": forecast['wind']['speed']
        }
        forecast_list.append(forecast_item)

    return {
        "city": city,
        "forecast": forecast_list
    }

import random

def get_activity_list(weather, activity_type, limit):
    '''Returns a list of activities based on the weather condition'''
    activities = get_activities_from_db(weather)

    if isinstance(activities, dict) and "error" in activities:
        return activities

    if not activities:
        activity_type = 'all'

    if activity_type == 'outdoor':
        activity_list = activities.get('outdoor_activities', [])
    elif activity_type == 'indoor':
        activity_list = activities.get('indoor_activities', [])
    elif activity_type == 'all':
        outdoor_activities = activities.get('outdoor_activities', [])
        indoor_activities = activities.get('indoor_activities', [])
        activity_list = outdoor_activities + indoor_activities
    else:
        return {"error": "Invalid type. Use 'outdoor', 'indoor', or 'all'."}

    if not activity_list:
        return {"error": f"No {activity_type} activities found for {weather} weather."}

    try:
        limit = min(int(limit), len(activity_list))
    except ValueError:
        return {"error": "Invalid limit. Please provide a number."}

    random.shuffle(activity_list)
    selected_activities = activity_list[:limit]

    return {
        "weather": weather,
        "type": activity_type,
        "activities": selected_activities
    }

def get_activities_from_db(condition):
    '''Fetches activities from the MongoDB collection based on the weather condition'''
    try:
        activities_doc = mongo.db.activities.find_one()
        
        if activities_doc and "weather_conditions" in activities_doc:
            weather_conditions = activities_doc["weather_conditions"]
            
            if condition in weather_conditions:
                return weather_conditions[condition]
            else:
                return weather_conditions
        else:
            print("No activities document found in the database")
            return {"outdoor_activities": [], "indoor_activities": []}
    except Exception as e:
        print(f"An error occurred while fetching activities: {str(e)}")
        return {"error": f"Database operation failed: {str(e)}"}
