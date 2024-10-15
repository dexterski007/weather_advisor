#!/usr/bin/python

from app import create_app, mongo
from app import cache

app = create_app()
cache.init_app(app)

# Ensure MongoDB connection is established when the app starts
with app.app_context():
    mongo.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
