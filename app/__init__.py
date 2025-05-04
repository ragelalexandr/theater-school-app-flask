# File: __init__.py
# Path: my_flask_app/app/__init__.py

# Инициализация приложения и подключение расширений

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_object='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Импорт и регистрация blueprints, если они есть
    # from app.student import bp as student_bp
    # app.register_blueprint(student_bp, url_prefix='/student')
    # и т.д.
    
    return app
