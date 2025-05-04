# File: routes.py
# Path: my_flask_app/app/admin/routes.py

# Маршруты (управление данными о представлениях, курсах, преподавателях, студентах; модерация отзывов)
# File: routes.py
# Path: my_flask_app/app/admin/routes.py

from functools import wraps
from app.forms import ResetPasswordForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.models import TheatreShow, Course, User, Review
from app.admin import bp
from app.decorators import roles_required

# Обработка ошибок и уведомления внутри маршрутов
@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('student.profile'))
    user = User.verify_reset_token(token)
    if not user:
        flash('Неверный или устаревший токен.', 'warning')
        return redirect(url_for('student.reset_password_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Ваш пароль обновлен. Теперь вы можете войти.', 'success')
        return redirect(url_for('student.login'))
    return render_template('student/reset_password.html', title='Сброс пароля', form=form)

# Декоратор для проверки, что текущий пользователь – администратор
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Доступ разрешен только для администраторов.', 'danger')
            return redirect(url_for('student.login'))
        return f(*args, **kwargs)
    return decorated_function

# ================== 6.1. Административная панель ==================
@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    return render_template('admin/dashboard.html', title='Административная панель')

# ================== 6.2. Управление базами данных ==================

# ---- Театральные представления (CRUD для TheatreShow) ----
@bp.route('/theatre_shows')
@login_required
@admin_required
def theatre_shows():
    shows = TheatreShow.query.order_by(TheatreShow.show_date.desc()).all()
    return render_template('admin/theatre_shows.html', shows=shows, title='Театральные представления')

@bp.route('/theatre_shows/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_theatre_show():
    if request.method == 'POST':
        title = request.form.get('title')
        show_date = request.form.get('show_date')  # Формат: "YYYY-MM-DD HH:MM:SS"
        description = request.form.get('description')
        new_show = TheatreShow(title=title, show_date=show_date, description=description)
        db.session.add(new_show)
        db.session.commit()
        flash('Театральное представление добавлено.', 'success')
        return redirect(url_for('admin.theatre_shows'))
    return render_template('admin/add_theatre_show.html', title='Добавить представление')

@bp.route('/theatre_shows/edit/<int:show_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_theatre_show(show_id):
    show = TheatreShow.query.get_or_404(show_id)
    if request.method == 'POST':
        show.title = request.form.get('title')
        show.show_date = request.form.get('show_date')
        show.description = request.form.get('description')
        db.session.commit()
        flash('Данные представления обновлены.', 'success')
        return redirect(url_for('admin.theatre_shows'))
    return render_template('admin/edit_theatre_show.html', show=show, title='Редактировать представление')

@bp.route('/theatre_shows/delete/<int:show_id>', methods=['POST'])
@login_required
@admin_required
def delete_theatre_show(show_id):
    show = TheatreShow.query.get_or_404(show_id)
    db.session.delete(show)
    db.session.commit()
    flash('Представление удалено.', 'info')
    return redirect(url_for('admin.theatre_shows'))
    
# ---- Курсы (CRUD для Course) ----
@bp.route('/courses')
@login_required
@admin_required
def courses():
    courses = Course.query.order_by(Course.start_datetime.desc()).all()
    return render_template('admin/courses.html', courses=courses, title='Курсы')

@bp.route('/courses/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_course():
    if request.method == 'POST':
        title = request.form.get('title')
        teacher_id = request.form.get('teacher_id')
        start_datetime = request.form.get('start_datetime')
        end_datetime = request.form.get('end_datetime')
        available = request.form.get('available') == 'true'
        new_course = Course(title=title, teacher_id=teacher_id,
                            start_datetime=start_datetime, end_datetime=end_datetime, available=available)
        db.session.add(new_course)
        db.session.commit()
        flash