import os

class Config:
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "d3368120080f668ea9f5c0a56b994aa0")
    ACTIVITY_SUGGESTIONS = ["Hiking", "Running", "Swimming", "Indoor Gym", "Reading", "Cycling"]
