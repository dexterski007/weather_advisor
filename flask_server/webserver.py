#!/usr/bin/python3

from flask import Flask, jsonify
from flask_server.map import get_coordinates
from flask_server.weather import get_weather


def webserver():
    app = Flask(__name__)

    @app.route('/')
    def welcome():
        return jsonify({ 'Message': 'Welcome visitor!'})
    
    @app.route('/get_coordinates/<location>')
    def coordinates(location):
        coordinates = get_coordinates(location)
        longitude = coordinates[0]['lon']
        latitude = coordinates[0]['lat']
        weather = get_weather(longitude, latitude)
        condition = weather[0][11]['description']
        return jsonify({'weather': condition})
    
    app.run('0.0.0.0', 5000)
