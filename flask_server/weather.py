#!/usr/bin/python3

import requests


API_KEY = 'd3368120080f668ea9f5c0a56b994aa0'

def get_weather(lon, lat):
    weath_api = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}'
    req = requests.get(weath_api)
    if req.status_code == 200:
        data = req.json()
        return data
    return None
