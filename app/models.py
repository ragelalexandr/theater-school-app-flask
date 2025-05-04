# File: models.py
# Path: my_flask_app/app/models.py

# Определение моделей (User, Course, Registration, PortfolioItem, Review, TheatreShow и т.д.)

# File: models.py
# Path: /my_flask_app/app/models.py

from datetime import datetime, date
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager


# File: models.py
# Path: /my_flask_app/app/models.py

# Функция загрузки пользователя для Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# =====================================================================
# Модель пользователя
# Эта модель используется для всех типов пользователей: студент, преподаватель, администратор.
# Дополнительное поле role используется для разграничения прав доступа.
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='student', nullable=False)  # Возможные значения: 'student', 'teacher', 'admin'
    name = db.Column(db.String(64))
    contact_info = db.Column(db.String(120))
    
    # Новое поле для фото профиля:
    profile_picture = db.Column(db.String(140), default='default_profile.jpg')

    # Отношения:
    # Один студент может иметь множество записей на курсы
    registrations = db.relationship('Registration', backref='student', lazy='dynamic')
    # Портфолио пользователя
    portfolio_items = db.relationship('PortfolioItem', backref='owner', lazy='dynamic')
    # Отзывы, оставленные пользователем (например, студентами)
    reviews = db.relationship('Review', backref='author', lazy='dynamic')
    # Если пользователь — преподаватель, он может вести курсы (см. Course.teacher)
    
    def set_password(self, password):
        """Устанавливает пароль, сохраняя хеш."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Проверяет введённый пароль."""
        return check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        # s.dumps() возвращает строку, если используем Python 3
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=expires_sec)
            user_id = data['user_id']
        except Exception:
            return None
        return User.query.get(user_id)




# =====================================================================
# Модель курса
# Эта модель хранит данные о курсах, включая название, расписание, ссылку на преподавателя и статус доступности.
class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    # Расписание курса: дата и время начала и окончания
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    available = db.Column(db.Boolean, default=True)
    
    # Внешний ключ на преподавателя (который является пользователем с ролью 'teacher')
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # Отношение для удобного доступа к данным преподавателя
    teacher = db.relationship('User', foreign_keys=[teacher_id], backref='courses_taught')
    
    # Один курс может иметь множество регистраций студентов
    registrations = db.relationship('Registration', backref='course', lazy='dynamic')
    
    def __repr__(self):
        return f'<Course {self.title}>'


# =====================================================================
# Модель регистрации на курс
# Хранит запись студента на курс с указанием типа прохождения, выбранного периода и статуса заявки.
class Registration(db.Model):
    __tablename__ = 'registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    # Ссылка на студента, который записался
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Ссылка на курс, на который записался студент
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    # Тип прохождения: 'personal' (персональное) или 'group' (парное/групповое)
    registration_type = db.Column(db.String(20))
    # Даты начала и окончания курса (или периода записи)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    # Статус заявки: например, 'pending', 'confirmed', 'completed'
    status = db.Column(db.String(20), default='pending')
    
    def __repr__(self):
        return f'<Registration Student:{self.student_id}, Course:{self.course_id}>'


# =====================================================================
# Модель элемента портфолио
# Предназначена для хранения данных о достижениях студента: изображения, видео, текстовые описания.
class PortfolioItem(db.Model):
    __tablename__ = 'portfolio_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Тип элемента: 'image', 'video' или 'text'
    item_type = db.Column(db.String(20))
    # Содержимое: для изображений/видео — путь или URL; для текста — само описание
    content = db.Column(db.Text)
    # Краткое описание или заголовок элемента
    description = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PortfolioItem User:{self.user_id}, Type:{self.item_type}>'


# =====================================================================
# Модель отзывов
# Хранит отзывы, оставленные студентами, с возможностью модерации.
class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    # Ссылка на студента, автора отзыва
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Можно привязать отзыв к конкретному курсу
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)
    content = db.Column(db.Text, nullable=False)
    # Рейтинг отзыва (например, от 1 до 5)
    rating = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Флаг, говорящий о том, прошёл ли отзыв модерацию
    moderated = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Review Student:{self.student_id}, Course:{self.course_id}>'


# =====================================================================
# Модель театрального представления
# Данные для управления представлениями для администратора.
class TheatreShow(db.Model):
    __tablename__ = 'theatre_shows'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    # Дата и время проведения представления
    show_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<TheatreShow {self.title} on {self.show_date}>'
