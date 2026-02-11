import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET = os.getenv('JWT_SECRET', 'default_jwt_secret')
    SERVER_NAME = os.getenv('SERVER_NAME', 'localhost:5000')
    CACHE_TTL = int(os.getenv('CACHE_TTL', 300))

class DevelopmentConfig(Config):
    DEBUG = True
    STRAVA_CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
    STRAVA_CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')

class ProductionConfig(Config):
    DEBUG = False
    STRAVA_CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
    STRAVA_CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')

class TestingConfig(Config):
    TESTING = True
    STRAVA_CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
    STRAVA_CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
