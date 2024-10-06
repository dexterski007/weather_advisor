#!/usr/bin/python3

from flask import Flask, jsonify
from flask_server.map import get_coordinates


def webserver():
    app = Flask(__name__)

    @app.route('/')
    def welcome():
        return jsonify({ 'Message': 'Welcome visitor!'})
    
    @app.route('/get_coordinates/<location>')
    def coordinates(location):
        coordinates = get_coordinates(location)
        return jsonify({'coordinates': coordinates})
    
    app.run('0.0.0.0', 5000)
