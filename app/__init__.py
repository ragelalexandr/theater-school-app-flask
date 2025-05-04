# File: __init__.py
# Path: theater-school-app-flask/app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Импорт расширений должен происходить до импортов blueprint-ов
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# Импорт blueprint-ов
from app.student import bp as student_bp
from app.teacher import bp as teacher_bp
from app.admin import bp as admin_bp

# Импорт глобальных обработчиков ошибок
# Вы НЕ должны вызывать register_error_handlers здесь, пока app не создан
from app import errors

def create_app(config_object='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Регистрация blueprint-ов
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(teacher_bp, url_prefix='/teacher')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Регистрируем обработчики ошибок после создания приложения
    errors.register_error_handlers(app)
    
    return app
