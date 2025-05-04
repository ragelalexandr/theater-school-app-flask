# File: __init__.py
# Path: my_flask_app/app/__init__.py

# Инициализация приложения и подключение расширений

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.student import bp as student_bp
from app.teacher import bp as teacher_bp
from app.admin import bp as admin_bp
from app import errors

from app.student import routes

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_object='app.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Регистрация blueprint'ов
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(teacher_bp, url_prefix='/teacher')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Регистрация глобальных обработчиков ошибок


    return app
