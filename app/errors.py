# File: errors.py
# Path: theater-school-app-flask/app/errors.py

from flask import render_template
# Удалите следующую строку, чтобы избежать циклического импорта:
# from app import app  

# Определите обработчики ошибок с декораторами,
# если вы хотите их зарегистрировать в глобальном пространстве.
# Но удобнее зарегистрировать их внутри функции, принимающей объект app.

def not_found_error(error):
    return render_template('errors/404.html'), 404

def internal_error(error):
    # При необходимости можно выполнить db.session.rollback()
    return render_template('errors/500.html'), 500

# Опционально можно добавить функцию для регистрации обработчиков:
def register_error_handlers(app):
    app.register_error_handler(404, not_found_error)
    app.register_error_handler(500, internal_error)
