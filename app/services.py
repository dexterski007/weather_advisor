import requests
from flask import current_app
import random
from app import cache
from .utils import get_combined_activities


@cache.cached(timeout=300, key_prefix='weather_data_{city}')
def get_weather_data(city):
    '''Fetches weather data from OpenWeatherMap API'''
    api_key = current_app.config['WEATHER_API_KEY']
    url = f"http://api.openweathermap.org/data/2.5/weather?\
        q={city}&appid={api_key}&units=metric"

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
    imported = get_combined_activities()
    print(imported)
    activities_json = imported['weather_activities']

    if temp > 298 and 'water' in activities_json[condition]:
        activity_list = activities_json[condition]['outdoor_activities']
    elif temp < 283 or wind_speed > 10:
        activity_list = activities_json[condition]['indoor_activities']
    else:
        if 'outdoor_activities' in activities_json[condition]:
            activity_list = activities_json[condition]['outdoor_activities']
        else:
            activity_list = activities_json[condition]['indoor_activities']

    return random.choice(activity_list)


@cache.cached(timeout=300, key_prefix='forecast_data_{city}')
def get_weather_forecast(city, days):
    '''Fetches weather forecast data from OpenWeatherMap API'''
    weather_api_key = current_app.config['WEATHER_API_KEY']
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?\
                    q={city}&cnt={int(days)}&\
                        appid={weather_api_key}&units=metric"

    response = requests.get(forecast_url)

    if response.status_code != 200:
        return ({"error": "Unable to fetch weather data."})

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

    return ({
        "city": city,
        "forecast": forecast_list
    })


def get_activity_list(weather, activity_type, limit):
    '''Returns a list of activities based on the weather condition'''

    imported = get_combined_activities()
    print(imported)
    activities_json = imported['weather_activities']

    if weather not in activities_json:
        return {"error": f"No activities found for\
                 weather condition: {weather}"}

    if activity_type == 'outdoor':
        activity_list = activities_json[weather].get('outdoor_activities', [])
    elif activity_type == 'indoor':
        activity_list = activities_json[weather].get('indoor_activities', [])
    elif activity_type == 'all':
        outdoor_activities = activities_json[weather].\
            get('outdoor_activities', [])
        indoor_activities = activities_json[weather].\
            get('indoor_activities', [])
        activity_list = outdoor_activities + indoor_activities
    else:
        return ({"error": "Invalid type. Use 'outdoor' or 'indoor' or 'all'."})

    if not activity_list:
        return {"error": f"No {activity_type} activities\
                found for {weather} weather."}

    limit = min(int(limit), len(activity_list))
    random.shuffle(activity_list)
    selected_activities = activity_list[:limit]

    return ({
        "weather": weather,
        "type": activity_type,
        "activities": selected_activities
    })
