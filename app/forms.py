# File: forms.py
# Path: my_flask_app/app/forms.py

# Формы (регистрация, логин, изменение профиля, запись на курс и проч.)

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import Length


class RegistrationForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Подтвердите пароль', validators=[
        DataRequired(), EqualTo('password', message='Пароли должны совпадать.')
    ])
    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Пользователь с таким email уже существует.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField('Запросить восстановление пароля')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Нет учетной записи с этим email.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Новый пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Подтвердите пароль', validators=[
        DataRequired(), EqualTo('password', message='Пароли должны совпадать.')
    ])
    submit = SubmitField('Сбросить пароль')


class UpdateProfileForm(FlaskForm):
    name = StringField('Имя', validators=[Length(max=64)])
    contact_info = StringField('Контактная информация', validators=[Length(max=120)])
    # Если хотите ограничить тип файлов, можно добавить FileAllowed, например:
    # picture = FileField('Загрузить фотографию профиля', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    picture = FileField('Загрузить фотографию профиля')
    submit = SubmitField('Сохранить изменения')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Текущий пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[DataRequired(), Length(min=6)])
    confirm_new_password = PasswordField('Подтвердите новый пароль', validators=[
        DataRequired(), EqualTo('new_password', message='Пароли должны совпадать.')
    ])
    submit = SubmitField('Изменить пароль')

class DeleteAccountForm(FlaskForm):
    submit = SubmitField('Удалить аккаунт')

# Форма для записи на курс
class CourseRegistrationForm(FlaskForm):
    course = SelectField('Курс', coerce=int, validators=[DataRequired()])
    registration_type = SelectField('Тип прохождения', choices=[('personal', 'Персональное'), ('group', 'Групповое')], validators=[DataRequired()])
    start_date = DateField('Дата начала', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('Дата окончания', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Записаться')

# Форма для создания и редактирования элемента портфолио
class PortfolioItemForm(FlaskForm):
    item_type = SelectField('Тип элемента', choices=[('image', 'Изображение'), ('video', 'Видео'), ('text', 'Текст')], validators=[DataRequired()])
    content = StringField('Содержимое', validators=[DataRequired()])
    description = StringField('Описание', validators=[Length(max=256)])
    submit = SubmitField('Сохранить')

# Форма для оставления отзыва
class ReviewForm(FlaskForm):
    course = SelectField('Курс', coerce=int, validators=[DataRequired()])
    rating = SelectField('Оценка', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    content = TextAreaField('Отзыв', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Оставить отзыв')
