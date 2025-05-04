# File: decorators.py
# Path: /my_flask_app/app/decorators.py

from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def roles_required(*roles):
    """
    Декоратор для проверки, что текущий пользователь имеет одну из указанных ролей.
    Пример использования:
    
        @app.route('/admin_only')
        @login_required
        @roles_required('admin')
        def admin_only():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                flash("Доступ разрешён только для пользователей с необходимыми правами: " + ", ".join(roles), "danger")
                # Можно перенаправлять на страницу входа или на главную страницу
                return redirect(url_for('student.login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
