#!/usr/bin/python

from app import create_app
from app import cache


app = create_app()
cache.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
