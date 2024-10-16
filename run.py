#!/usr/bin/python
"""Run the Flask app."""

from app import create_app, mongo
from app import cache

app = create_app()
cache.init_app(app)

with app.app_context():
    mongo.init_app(app)

if __name__ == '__main__':
    '''Run the app.'''
    app.run(host='0.0.0.0', port=5000)
