# File: routes.py
# Path: my_flask_app/app/student/routes.py

# Маршруты (регистрация, профиль, расписание, запись на курсы, портфолио, история, отзывы)

from flask import render_template, url_for, flash, redirect, request, current_app
from werkzeug.utils import secure_filename
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.models import User, Course, Registration, PortfolioItem, Review
from app.forms import (
    RegistrationForm, LoginForm,
    RequestResetForm, ResetPasswordForm,
    UpdateProfileForm, ChangePasswordForm, DeleteAccountForm,
    CourseRegistrationForm, PortfolioItemForm, ReviewForm
)
from app.email import send_reset_email  # Предполагается, что функция для отправки письма реализована
from app.student import bp  # импортировать blueprint
from app.decorators import roles_required



# Реализация декоратора для проверки ролей
@bp.route('/dashboard')
@login_required
@roles_required('student')
def student_dashboard():
    return render_template('student/dashboard.html', title='Панель студента')


# ---------------------- Регистрация ----------------------
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('student.profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, role='student')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация успешна. Теперь вы можете войти в систему.', 'success')
        return redirect(url_for('student.login'))
    return render_template('student/register.html', title='Регистрация', form=form)

# ---------------------- Авторизация ----------------------
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('student.profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Вход выполнен успешно.', 'success')
            return redirect(next_page) if next_page else redirect(url_for('student.profile'))
        else:
            flash('Неверный email или пароль.', 'danger')
    return render_template('student/login.html', title='Вход', form=form)

# Выход из системы
@bp.route('/logout')
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('student.login'))

# ---------------------- Восстановление пароля ----------------------

# Запрос на восстановление пароля: форма ввода email
@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('student.profile'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash('На вашу почту отправлено письмо с инструкциями по восстановлению пароля.', 'info')
            return redirect(url_for('student.login'))
    return render_template('student/reset_password_request.html', title='Восстановление пароля', form=form)

# Форма для ввода нового пароля (после перехода по ссылке с токеном)
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

# ---------------------- Настройки профиля ----------------------
@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.contact_info = form.contact_info.data
        
        # Обработка загрузки файла с фотографией
        if form.picture.data:
            filename = secure_filename(form.picture.data.filename)
            picture_path = current_app.root_path + '/static/profile_pics/' + filename
            form.picture.data.save(picture_path)
            # Пример: сохраняем путь в дополнительное поле profile_image (добавьте его в модель User, если требуется)
            current_user.profile_image = 'profile_pics/' + filename
        
        db.session.commit()
        flash('Ваш профиль обновлен.', 'success')
        return redirect(url_for('student.profile'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.contact_info.data = current_user.contact_info
    return render_template('student/profile.html', title='Профиль', form=form)

# Смена пароля
@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Неверный текущий пароль.', 'danger')
        else:
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Пароль успешно изменен.', 'success')
            return redirect(url_for('student.profile'))
    return render_template('student/change_password.html', title='Смена пароля', form=form)

# Удаление аккаунта
@bp.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    form = DeleteAccountForm()
    if form.validate_on_submit():
        user = current_user
        logout_user()
        db.session.delete(user)
        db.session.commit()
        flash('Ваш аккаунт был удален.', 'info')
        return redirect(url_for('student.register'))
    return render_template('student/delete_account.html', title='Удалить аккаунт', form=form)

# ----- 4.3. Просмотр расписания -----
@bp.route('/schedule')
@login_required
def schedule():
    courses = Course.query.order_by(Course.start_datetime.asc()).all()
    return render_template('student/schedule.html', title='Расписание курсов', courses=courses)

# ----- 4.3. Запись на курс -----
@bp.route('/register_course', methods=['GET', 'POST'])
@login_required
def register_course():
    form = CourseRegistrationForm()
    # Заполняем список доступных курсов: [ (course_id, course_title), ... ]
    form.course.choices = [(course.id, course.title) for course in Course.query.order_by(Course.title).all()]
    
    if form.validate_on_submit():
        registration = Registration(
            student_id = current_user.id,
            course_id = form.course.data,
            registration_type = form.registration_type.data,
            start_date = form.start_date.data,
            end_date = form.end_date.data,
            status = 'pending'
        )
        db.session.add(registration)
        db.session.commit()
        flash('Ваша заявка на курс успешно отправлена!', 'success')
        return redirect(url_for('student.history'))
    return render_template('student/register_course.html', title='Запись на курс', form=form)

# ----- 4.4. Создание и редактирование портфолио -----
@bp.route('/portfolio', methods=['GET', 'POST'])
@login_required
def portfolio():
    form = PortfolioItemForm()
    if form.validate_on_submit():
        item = PortfolioItem(
            user_id = current_user.id,
            item_type = form.item_type.data,
            content = form.content.data,
            description = form.description.data
        )
        db.session.add(item)
        db.session.commit()
        flash('Элемент портфолио добавлен', 'success')
        return redirect(url_for('student.portfolio'))
    items = PortfolioItem.query.filter_by(user_id=current_user.id).all()
    return render_template('student/portfolio.html', title='Портфолио', form=form, items=items)

@bp.route('/portfolio/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_portfolio_item(item_id):
    item = PortfolioItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash('Нет прав для редактирования этого элемента.', 'danger')
        return redirect(url_for('student.portfolio'))
    form = PortfolioItemForm()
    if form.validate_on_submit():
        item.item_type = form.item_type.data
        item.content = form.content.data
        item.description = form.description.data
        db.session.commit()
        flash('Элемент портфолио обновлен', 'success')
        return redirect(url_for('student.portfolio'))
    elif request.method == 'GET':
        form.item_type.data = item.item_type
        form.content.data = item.content
        form.description.data = item.description
    return render_template('student/edit_portfolio_item.html', title='Редактировать портфолио', form=form, item=item)

@bp.route('/portfolio/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_portfolio_item(item_id):
    item = PortfolioItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash('Нет прав для удаления этого элемента.', 'danger')
        return redirect(url_for('student.portfolio'))
    db.session.delete(item)
    db.session.commit()
    flash('Элемент портфолио удален', 'info')
    return redirect(url_for('student.portfolio'))

# ----- 4.5. Просмотр истории записей -----
@bp.route('/history')
@login_required
def history():
    registrations = Registration.query.filter_by(student_id=current_user.id).order_by(Registration.id.desc()).all()
    return render_template('student/history.html', title='История записей', registrations=registrations)

# ----- 4.5. Оставление отзывов -----
@bp.route('/leave_review', methods=['GET', 'POST'])
@login_required
def leave_review():
    form = ReviewForm()
    # Заполняем список курсов, на которые студент записался
    form.course.choices = [(reg.course.id, reg.course.title) for reg in Registration.query.filter_by(student_id=current_user.id).all()]
    
    if form.validate_on_submit():
        review = Review(
            student_id = current_user.id,
            course_id = form.course.data,
            rating = int(form.rating.data),
            content = form.content.data,
            moderated = False  # Отзыв будет опубликован после модерации
        )
        db.session.add(review)
        db.session.commit()
        flash('Отзыв отправлен! После модерации он будет опубликован.', 'success')
        return redirect(url_for('student.history'))
    return render_template('student/leave_review.html', title='Оставить отзыв', form=form)
