import requests
from flask import current_app
from .utils import kelvin_to_celsius
import json

def get_weather_data(city):
    api_key = current_app.config['WEATHER_API_KEY']
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Unable to fetch weather data"}
    
    data = response.json()
    with open("data.json", "w") as export:
        export.write(json.dumps(data))
    weather = {
        "description": data["weather"][0]["description"],
        "temperature": kelvin_to_celsius(data["main"]["temp"]),
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"]
    }
    return weather

def suggest_activity(weather_data):
    temp = weather_data['temperature']
    description = weather_data['description']
    
    # Simple recommendation based on weather
    if 'rain' in description or 'storm' in description:
        return "Indoor Gym"
    elif temp > 298:  # If temperature is above ~25°C
        return "Swimming"
    elif temp < 288:  # If temperature is below ~15°C
        return "Reading"
    else:
        return "Running"
