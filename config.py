# File: config.py
# Path: /my_flask_app/config.py

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Добавьте другие переменные конфигурации по необходимости
