# File: errors.py
# Path: theater-school-app-flask/app/errors.py

from flask import render_template

def not_found_error(error):
    return render_template('errors/404.html'), 404

def internal_error(error):
    # При необходимости можно выполнить db.session.rollback()
    return render_template('errors/500.html'), 500

def register_error_handlers(app):
    app.register_error_handler(404, not_found_error)
    app.register_error_handler(500, internal_error)

