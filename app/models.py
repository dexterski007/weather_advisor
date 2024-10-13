#!/usr/bin/python3

import requests
from .utils import MAP_API_KEY


def get_coordinates(location):
    gmap_api = f'https://geocode.maps.co/search?q={location}&api_key={MAP_API_KEY}'
    req = requests.get(gmap_api)
    if req.status_code == 200:
        data = req.json()
        return data
    return None
