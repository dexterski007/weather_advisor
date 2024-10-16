import requests
from flask import current_app, request
import random
from app import cache, mongo
from .utils import get_combined_activities
import re


def weather_data_key():
    city = request.args.get('city')
    return f"forecast_data_{city}"


@cache.cached(timeout=300, key_prefix=weather_data_key)
def get_weather_data(city):
    '''Fetches weather data from OpenWeatherMap API'''
    api_key = current_app.config['WEATHER_API_KEY']
    url = f"http://api.openweathermap.org/data/2.5/\
        weather?q={city}&appid={api_key}&units=metric"

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
        activity_list = activities_json.get(
            'outdoor_activities', activities_json.get('indoor_activities', []))

    return random.choice(activity_list) if activity_list else None


def make_cache_key():
    city = request.args.get('city')
    days = request.args.get('days')
    return f"forecast_data_{city}_{days}"


@cache.cached(timeout=300, key_prefix=make_cache_key)
def get_weather_forecast(city, days):
    '''Fetches weather forecast data from OpenWeatherMap API'''
    weather_api_key = current_app.config['WEATHER_API_KEY']
    forecast_url = f"http://api.openweathermap.org/data/2.5/\
        forecast?q={city}&cnt={int(days)}&appid={weather_api_key}&units=metric"

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


def get_activity_list(weather, activity_type, limit):
    '''Returns a list of activities based on
    the weather condition and activity type'''
    activities = get_activities_from_db(weather)

    if isinstance(activities, dict) and "error" in activities:
        return activities

    if weather is None:
        all_activities = {"outdoor_activities": [], "indoor_activities": []}
        for condition, acts in activities.items():
            all_activities['outdoor_activities'] += \
                acts.get('outdoor_activities', [])
            all_activities['indoor_activities'] += \
                acts.get('indoor_activities', [])
        activities = all_activities

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
        return {"error": f"No {activity_type} activities found."}

    try:
        if limit is not None:
            limit = min(int(limit), len(activity_list))
            random.shuffle(activity_list)
            activity_list = activity_list[:limit]
    except ValueError:
        return {"error": "Invalid limit. Please provide a number."}

    return {
        "weather": weather if weather else "all",
        "type": activity_type,
        "activities": activity_list
    }


def get_activities_from_db(condition=None):
    '''Fetches activities from the MongoDB
    collection based on the weather condition'''
    try:
        activities_doc = mongo.db.activities.find_one()

        if activities_doc and "weather_conditions" in activities_doc:
            weather_conditions = activities_doc["weather_conditions"]

            if condition:
                return weather_conditions.get(condition, {})
            else:
                return weather_conditions
        else:
            print("No activities document found in the database")
            return {"outdoor_activities": [], "indoor_activities": []}
    except Exception as e:
        print(f"An error occurred while fetching activities: {str(e)}")
        return {"error": f"Database operation failed: {str(e)}"}


def search_activities_in_db(activity_query, activity_type=None):
    '''Performs a text search in MongoDB for
    the given activity query and activity type'''
    try:
        search_filter = {
            "$text": {"$search": activity_query}
        }

        activities = mongo.db.activities.find(search_filter,
                                              {"score":
                                               {"$meta": "textScore"}}).sort(
                                                   [("score",
                                                     {"$meta": "textScore"})])

        activity_list = []
        for activity_doc in activities:
            for weather, condition in \
               activity_doc.get('weather_conditions', {}).items():
                if activity_type is None or activity_type == 'outdoor':
                    for activity in condition.get('outdoor_activities', []):
                        if re.search(r'\b' + re.escape(activity_query) +
                                     r'\b', activity, re.IGNORECASE):
                            activity_list.append({
                                "activity": activity,
                                "type": "outdoor",
                                "weather": weather
                            })

                if activity_type is None or activity_type == 'indoor':
                    for activity in condition.get('indoor_activities', []):
                        if re.search(r'\b' + re.escape(activity_query) +
                                     r'\b', activity, re.IGNORECASE):
                            activity_list.append({
                                "activity": activity,
                                "type": "indoor",
                                "weather": weather
                            })

        return activity_list if activity_list else None

    except Exception as e:
        print(f"Error during search: {str(e)}")
        return {"error": f"Search operation failed: {str(e)}"}
