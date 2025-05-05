# File: config.py
# Path: my_flask_app/app/config.py

# Конфигурация (SECRET_KEY, параметры БД, настройки Flask-Mail и др.)

# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'сложная_и_уникальная_строка'
    # Другие настройки ...
