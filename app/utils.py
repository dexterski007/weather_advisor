# Description: This file contains utility
# functions that are used in the application.

from flask import current_app
import json

app = current_app

def kelvin_to_celsius(temp):
    ''' deprecated, using builtin api endpoint instead '''
    new_temp = round(temp - 273.15, 3)
    return new_temp

def get_combined_activities():
    system_activities = current_app.config['ACTIVITIES_JSON']
    user_activities = current_app.config['USER_ACTIVITIES_JSON']

    if not user_activities:
        return system_activities

    combined_activities = system_activities.copy()

    for weather, activities in user_activities['weather_conditions'].items():
        if weather in combined_activities['weather_conditions']:
            combined_activities['weather_conditions'][weather]['outdoor_activities'].extend(
                activities.get('outdoor_activities', [])
            )
            combined_activities['weather_conditions'][weather]['indoor_activities'].extend(
                activities.get('indoor_activities', [])
            )
        else:
            combined_activities['weather_conditions'][weather] = activities

    return combined_activities
