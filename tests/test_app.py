# File: test_app.py
# Path: /my_flask_app/tests/test_app.py

import os
import tempfile
import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    # Создаем временную базу данных для тестов (sqlite:memory или temp-файл)
    db_fd, db_path = tempfile.mkstemp()
    app = create_app('app.config.TestingConfig')  # создайте конфигурацию для тестов

    # Переопределяем конфигурацию тестового приложения
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + db_path,
    })

    with app.app_context():
        db.create_all()
        # Можно создать тестового пользователя
        test_user = User(email='test@example.com', role='student')
        test_user.set_password('testpass')
        db.session.add(test_user)
        db.session.commit()
    yield app

    # Очистка после теста
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page(client):
    # Пример простого теста для главной страницы (зависит от вашей реализации маршрутов)
    response = client.get('/')
    assert response.status_code in (200, 302)  # если главная страница редирект или 200 OK

def test_registration_page(client):
    # Пример теста для страницы регистрации
    response = client.get('/student/register')
    assert response.status_code == 200
    assert 'Регистрация'.encode("utf-8") in response.data

def test_invalid_login(client):
    # Пример теста для неверного входа
    response = client.post('/student/login', data={
        'email': 'wrong@example.com',
        'password': 'wrong'
    }, follow_redirects=True)
    assert 'Неверный email или пароль'.encode("utf-8") in response.data
