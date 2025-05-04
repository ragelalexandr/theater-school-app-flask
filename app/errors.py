# File: errors.py
# Path: /my_flask_app/app/errors.py

from flask import render_template
from app import app  # Если используете фабрику приложения, можно импортировать объект приложения другим способом

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    # При необходимости можно сделать откат транзакций (db.session.rollback())
    return render_template('errors/500.html'), 500
