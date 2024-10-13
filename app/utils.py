# Description: This file contains utility
# functions that are used in the application.

def kelvin_to_celsius(temp):
    ''' deprecated, using builtin api endpoint instead '''
    new_temp = round(temp - 273.15, 3)
    return new_temp
