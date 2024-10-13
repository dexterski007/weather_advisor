#!/usr/bin/python3

import requests
from flask import current_app


def get_coordinates(location):
    '''Fetches the coordinates of a location using the Google Maps API'''
    MAP_API_KEY = current_app.config['MAP_API_KEY']
    gmap_api = f'https://geocode.maps.co/search?\
                q={location}&api_key={MAP_API_KEY}'
    response = requests.get(gmap_api)
    if response.status_code != 200:
        return ({"error": "Unable to fetch geocoding data."})

    geocoding_data = response.json()
    return (geocoding_data)
