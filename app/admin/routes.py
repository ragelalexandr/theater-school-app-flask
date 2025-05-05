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
from datetime import datetime




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
@roles_required('admin')
def dashboard():
    shows = TheatreShow.query.order_by(TheatreShow.show_date.desc()).all()
    courses = Course.query.order_by(Course.start_datetime.desc()).all()
    teachers = User.query.filter_by(role='teacher').order_by(User.name).all()
    students = User.query.filter_by(role='student').order_by(User.name).all()
    reviews = Review.query.filter_by(moderated=False).order_by(Review.created_at.desc()).all()
    return render_template('admin/dashboard.html',
                           title='Административная панель',
                           shows=shows,
                           courses=courses,
                           teachers=teachers,
                           students=students,
                           reviews=reviews)


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
        # Получаем строку, например "2025-07-06T18:00"
        show_date_str = request.form.get('show_date')
        # Преобразуем строку в объект datetime согласно формату, который возвращает flatpickr
        show_date = datetime.strptime(show_date_str, "%Y-%m-%dT%H:%M")
        description = request.form.get('description')
        
        new_show = TheatreShow(title=title, show_date=show_date, description=description)
        db.session.add(new_show)
        db.session.commit()
        flash('Театральное представление добавлено.', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_theatre_show.html', title='Добавить представление')


from datetime import datetime

@bp.route('/theatre_shows/edit/<int:show_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_theatre_show(show_id):
    show = TheatreShow.query.get_or_404(show_id)
    if request.method == 'POST':
        show.title = request.form.get('title')
        
        # Получаем строку даты и времени из формы, например "2025-08-12T18:00"
        show_date_str = request.form.get('show_date')
        if show_date_str:
            # Преобразуем строку в объект datetime. Формат должен соответствовать значению, возвращаемому вашим input.
            show.show_date = datetime.strptime(show_date_str, "%Y-%m-%dT%H:%M")
        
        show.description = request.form.get('description')
        db.session.commit()
        flash('Данные представления обновлены.', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/edit_theatre_show.html', show=show, title='Редактировать представление')


@bp.route('/theatre_shows/delete/<int:show_id>', methods=['POST'])
@login_required
@admin_required
def delete_theatre_show(show_id):
    show = TheatreShow.query.get_or_404(show_id)
    db.session.delete(show)
    db.session.commit()
    flash('Представление удалено.', 'info')
    return redirect(url_for('admin.dashboard'))

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

@bp.route('/teachers/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_teacher():
    if request.method == 'POST':
        # Обработка формы: получение данных формы, валидация и запись в базу данных.
        name = request.form.get('name')
        contact_info = request.form.get('contact_info')
        # Здесь добавьте логику создания нового преподавателя.
        new_teacher = User(name=name, contact_info=contact_info, role='teacher')
        db.session.add(new_teacher)
        db.session.commit()
        flash('Преподаватель успешно добавлен.', 'success')
        return redirect(url_for('admin.teachers'))
    return render_template('admin/add_teacher.html', title='Добавить преподавателя')

@bp.route('/students/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_student():
    if request.method == 'POST':
        # Получите данные из формы
        name = request.form.get('name')
        email = request.form.get('email')
        contact_info = request.form.get('contact_info')
        # Создайте нового студента
        new_student = User(name=name, email=email, contact_info=contact_info, role='student')
        db.session.add(new_student)
        db.session.commit()
        flash('Студент успешно добавлен.', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_student.html', title='Добавить студента')

@bp.route('/students/edit/<int:student_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_student(student_id):
    student = User.query.get_or_404(student_id)
    if request.method == 'POST':
        # Получаем данные из формы и обновляем запись студента
        student.name = request.form.get('name')
        student.email = request.form.get('email')
        student.contact_info = request.form.get('contact_info')
        db.session.commit()
        flash('Данные студента обновлены.', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/edit_student.html', student=student, title='Редактировать студента')

@bp.route('/students/delete/<int:student_id>', methods=['POST'])
@login_required
@admin_required
def delete_student(student_id):
    student = User.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash('Студент успешно удалён.', 'info')
    return redirect(url_for('admin.dashboard'))

