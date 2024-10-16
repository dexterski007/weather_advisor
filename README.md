Weather Advisor API

Weather Advisor is a Flask-based API service that recommends activities based on current weather conditions in a specified city. The API also offers endpoints for retrieving weather forecasts, geolocation data, and managing a collection of activities.
Demo

A live demo of the Weather Advisor API is accessible at: bmworks.tech
Table of Contents

    Features
    Installation
    API Endpoints
        Welcome
        Recommend Activity
        Weather Forecast
        Get Activities
        Random Activity
        Get Weather
        Search Activities
        Geocoding
        Add Activity
        Remove Activity
    Curl Command Examples
    Technologies Used
    License

Features

    Recommend activities based on real-time weather conditions.
    Retrieve weather forecasts for a given city.
    Fetch or search for activities based on weather, type (indoor/outdoor), or user-defined criteria.
    Manage activities by adding or removing them from the MongoDB database.
    Get geolocation data for a specific city.

Installation

To run this project locally, follow these steps:

    Clone the repository:

    bash

git clone https://github.com/dexterski007/weather_advisor
cd weather_advisor

Install dependencies:

sudo bash populate_activities.sh
git clone https://github.com/dexterski007/weather_advisor
cd weather_advisor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
python run.py

makefile

FLASK_APP=run.py
FLASK_ENV=development
MONGO_URI=mongodb://localhost:27017/weather_advisor
WEATHER_API_KEY=your_openweathermap_api_key

Run the Flask application:

bash

    flask run

    Access the API at http://127.0.0.1:5000/.

API Endpoints
Welcome Message

    GET /
    Returns a welcome message for the API.
    Response:

    json

    {
        "message": "Welcome to the Weather Advisor API!"
    }

Recommend Activity

    GET /recommend?city={city}
    Recommends an activity based on the current weather in the specified city.
    Parameters:
        city (required): The name of the city to get weather data for.
    Response:

    json

    {
        "activity": "Hiking through the nearest nature trail"
    }

Weather Forecast

    GET /weather/forecast?city={city}&days={days}
    Fetches a weather forecast for a city for the specified number of days (default is 3).
    Parameters:
        city (required): The name of the city.
        days (optional): The number of forecast days (default is 3).
    Response:

    json

    {
        "city": "London",
        "forecast": [
            {"date": "2024-10-17", "weather": "sunny"},
            {"date": "2024-10-18", "weather": "rainy"},
            ...
        ]
    }

Get Activities

    GET /activities?weather={weather}&type={type}&limit={limit}
    Fetches a list of activities filtered by weather and type (indoor/outdoor).
    Parameters:
        weather (optional): The weather condition (e.g., sunny, rainy).
        type (optional): The type of activity (e.g., indoor, outdoor).
        limit (optional): Maximum number of activities to return.
    Response:

    json

    {
        "activities": [
            "Picnic in the park",
            "Cycling along the river",
            ...
        ]
    }

Random Activity

    GET /activities/random?weather={weather}&type={type}
    Fetches a random activity based on weather and activity type.
    Parameters:
        weather (optional): The weather condition (e.g., sunny, rainy).
        type (optional): The type of activity (e.g., indoor, outdoor).
    Response:

    json

    {
        "activity": "Indoor yoga session",
        "weather": "rainy",
        "type": "indoor"
    }

Get Weather

    GET /weather?city={city}
    Fetches current weather data for a specific city.
    Parameters:
        city (required): The name of the city.
    Response:

    json

    {
        "city": "New York",
        "weather": "clear",
        "temperature": 22
    }

Activity Search

    GET /activities/search?activity={activity}&type={type}
    Searches for activities by name and type.
    Parameters:
        activity (required): The activity name or keyword.
        type (optional): The type of activity (indoor/outdoor).
    Response:

    json

    {
        "activities": [
            "Mountain Biking",
            "Road Cycling"
        ]
    }

Geocoding

    GET /geocoding?city={city}
    Fetches the geographic coordinates (latitude and longitude) of a city.
    Parameters:
        city (required): The name of the city.
    Response:

    json

    {
        "city": "Paris",
        "latitude": 48.8566,
        "longitude": 2.3522
    }

Add Activity

    POST /activities/add
    Adds a new activity to the database.
    Request Body:

    json

{
    "weather": "sunny",
    "type": "outdoor",
    "activity": "Beach Volleyball"
}

Response:

json

    {
        "message": "Activity added successfully"
    }

Remove Activity

    DELETE /activities/remove
    Removes an activity from the database.
    Request Body:

    json

{
    "weather": "sunny",
    "type": "outdoor",
    "activity": "Beach Volleyball"
}

Response:

json

    {
        "message": "Activity removed successfully"
    }

Curl Command Examples

You can test the API using curl commands. Here are some examples:

    Welcome Message:

    bash

curl -X GET http://bmworks.tech/

Recommend Activity:

bash

curl -X GET "http://bmworks.tech/recommend?city=London"

Add Activity:

bash

    curl -X POST http://bmworks.tech/activities/add \
    -H "Content-Type: application/json" \
    -d '{"weather": "sunny", "type": "outdoor", "activity": "Beach Volleyball"}'

For a full list of curl commands, refer to the Curl Command Examples section.
Technologies Used

    Flask: Python micro web framework for building the API.
    MongoDB: NoSQL database for storing activities.
    OpenWeatherMap API: For fetching weather data.
    Flask-CORS: For handling Cross-Origin Resource Sharing.
    Flask-PyMongo: For integrating MongoDB with Flask.
    Flask-Caching: To cache weather data and improve performance.

License

This project is licensed under the MIT License. See the LICENSE file for more details.
