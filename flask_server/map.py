#!/usr/bin/python3

import requests

API_KEY = '67030414f409f872728511xbm4cc6ab'


def get_coordinates(location):
    gmap_api = f'https://geocode.maps.co/search?q={location}&api_key={API_KEY}'
    req = requests.get(gmap_api)
    if req.status_code == 200:
        data = req.json()
        return data
    return None
