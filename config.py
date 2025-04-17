# playlist-app/config.py

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'devkey123')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql:///playlist_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
