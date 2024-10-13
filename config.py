import os
import json

class Config:
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'd3368120080f668ea9f5c0a56b994aa0')
    MAP_API_KEY = os.getenv('MAP_API_KEY', '67030414f409f872728511xbm4cc6ab')
    with open('activities.json', 'r') as file:
        ACTIVITIES_JSON = json.load(file)
