# File: config.py
# Path: theater-school-app-flask/app/config.py

class Config:
    SECRET_KEY = 'your-secret-key'  # обязательно измените на надежный секретный ключ
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # настройте строку подключения к БД
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Добавьте другие переменные конфигурации, если требуется
