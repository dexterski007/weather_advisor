import os


class Config:
    '''Set Flask configuration variables'''
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY',
                                'your_api_key_here')
    MAP_API_KEY = os.getenv('MAP_API_KEY',
                            'your_api_key_here')
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    CACHE_REDIS_PORT = os.getenv("REDIS_PORT", 6379)
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = f"redis://{CACHE_REDIS_HOST}:{CACHE_REDIS_PORT}/0"
    CACHE_DEFAULT_TIMEOUT = 300

    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://127.0.0.1:27017/weather_db')
