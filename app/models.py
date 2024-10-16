#!/usr/bin/python3

import requests
from flask import current_app, request
from app import cache


def geocoding_data_key():
    city = request.args.get('city')
    return f"geocoding_data_{city}"


@cache.cached(timeout=300, key_prefix=geocoding_data_key)
def get_coordinates(location):
    '''Fetches the coordinates of a location using the geocode.maps.co API'''
    if not current_app:
        raise RuntimeError("No application context found.")

    MAP_API_KEY = current_app.config.get('MAP_API_KEY')
    if not MAP_API_KEY:
        raise ValueError("MAP_API_KEY not found in application configuration.")

    gmap_api = f'https://geocode.maps.co/search'
    params = {
        'q': location,
        'api_key': MAP_API_KEY
    }

    try:
        response = requests.get(gmap_api, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return {"error": f"Error fetching geocoding data: {str(e)}"}

    geocoding_data = response.json()

    if not geocoding_data:
        return {"error": "No geocoding data found for the given location."}

    if isinstance(geocoding_data, list) and geocoding_data:
        first_result = geocoding_data[0]
        return {
            "lat": first_result.get('lat'),
            "lon": first_result.get('lon')
        }
    else:
        return {"error": "Unexpected response format from geocoding API."}
