# File: __init__.py
# Path: theater-school-app-flask/app/admin/__init__.py

# Blueprint для административного функционала
from flask import Blueprint

bp = Blueprint('admin', __name__, url_prefix='/admin')

from app.admin import routes
