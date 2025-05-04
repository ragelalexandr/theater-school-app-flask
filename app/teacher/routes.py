# File: routes.py
# Path: my_flask_app/app/teacher/routes.py

# Маршруты (просмотр курсов, список студентов, управление записями студентов)

from functools import wraps
from app.forms import ResetPasswordForm
from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import Course, Registration, User
from app.teacher import bp
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

# Реализация декоратора для проверки ролей
@bp.route('/dashboard')
@login_required
@roles_required('teacher')
def teacher_dashboard():
    return render_template('teacher/dashboard.html', title='Панель преподавателя')


# Декоратор для проверки, что текущий пользователь – преподаватель
def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'teacher':
            flash('Доступ разрешен только для преподавателей.', 'danger')
            # Перенаправляем на страницу логина или другую подходящую страницу
            return redirect(url_for('student.login'))
        return f(*args, **kwargs)
    return decorated_function

# 5.2. Dashboard преподавателя: просмотр курсов, за которые отвечает преподаватель.
@bp.route('/dashboard')
@login_required
@teacher_required
def dashboard():
    # Получаем курсы, где current_user является преподавателем
    courses = Course.query.filter_by(teacher_id=current_user.id).order_by(Course.start_datetime.asc()).all()
    return render_template('teacher/dashboard.html', title='Панель управления', courses=courses)

# Просмотр списка студентов, записанных на конкретный курс
@bp.route('/course/<int:course_id>/registrations')
@login_required
@teacher_required
def course_registrations(course_id):
    course = Course.query.get_or_404(course_id)
    # Проверяем, что данный курс ведется текущим преподавателем
    if course.teacher_id != current_user.id:
        flash('У вас нет доступа к этому курсу.', 'danger')
        return redirect(url_for('teacher.dashboard'))
    # Получаем записи для данного курса
    registrations = Registration.query.filter_by(course_id=course.id).all()
    return render_template('teacher/course_registrations.html', title='Список записей', course=course, registrations=registrations)

# 5.3. Управление записями студентов: подтверждение или отклонение заявок.
@bp.route('/registration/<int:reg_id>/<string:action>', methods=['POST'])
@login_required
@teacher_required
def manage_registration(reg_id, action):
    registration = Registration.query.get_or_404(reg_id)
    # Проверяем, принадлежит ли курс, на который подана запись, текущему преподавателю
    if registration.course.teacher_id != current_user.id:
        flash('У вас нет полномочий для управления данной заявкой.', 'danger')
        return redirect(url_for('teacher.dashboard'))
    if action == 'confirm':
        registration.status = 'confirmed'
        flash('Запись подтверждена.', 'success')
    elif action == 'reject':
        registration.status = 'rejected'
        flash('Запись отклонена.', 'info')
    else:
        flash('Неподдерживаемое действие.', 'warning')
        return redirect(url_for('teacher.course_registrations', course_id=registration.course.id))
    db.session.commit()
    return redirect(url_for('teacher.course_registrations', course_id=registration.course.id))
