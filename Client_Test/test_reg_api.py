import pytest
import sys
import os

# Добавляем путь к корневой папке проекта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Client_Api.extensions import db
from Models.user import User
from werkzeug.security import generate_password_hash


@pytest.fixture(scope='module')
def test_client():
    from Client_Server.app import app
    from Client_Server.config import Config
    from Client_Api.extensions import db  # Проверьте, что это правильный импорт

    # Используем тестовую конфигурацию
    app.config.from_object(Config)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI_TEST  # Гарантируем, что используется тестовая база
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()  # Создаем таблицы для тестирования
            yield testing_client  # Клиент тестирования для использования в тестах



@pytest.fixture(scope='function')
def new_user():
    return User(
        email='test@example.com',
        password=generate_password_hash('password123'),
        role='student',
        first_name='John',
        last_name='Doe'
    )

@pytest.fixture(scope='function')
def init_database(test_client):
    # Эта фикстура будет использоваться для создания начальных данных в базе данных
    # Не создаем таблицы и не удаляем их, просто очищаем сессию
    yield db

def test_successful_registration(test_client):
    # Тест на успешную регистрацию
    response = test_client.post('/api/auth/register', data={
        'email': 'newuser@example.com',
        'password': 'password123',
        'role': 'student',
        'first_name': 'Jane',
        'last_name': 'Doe',
        'phone': '1234567890',
        'telegram_username': '@janedoe',
        'city': 'New York'
    })
    assert response.status_code == 201
    assert b'User registered successfully' in response.data

def test_missing_required_fields(test_client):
    # Тест на отсутствие обязательных полей
    response = test_client.post('/api/auth/register', data={
        'email': 'test@example.com',
        'role': 'student'
        # отсутствует пароль, имя и фамилия
    })
    assert response.status_code == 400
    assert b'Missing required fields' in response.data


def test_user_already_exists(test_client, init_database, new_user):
    # Тест на попытку зарегистрировать существующего пользователя
    with test_client.application.app_context():
        # Добавляем нового пользователя
        db.session.add(new_user)
        db.session.commit()

        # Повторная попытка регистрации с теми же данными
        response = test_client.post('/api/auth/register', data={
            'email': 'test@example.com',  # Уже существующий email
            'password': 'password123',
            'role': 'student',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '1234567890',
            'telegram_username': '@johndoe',
            'city': 'New York'
        })

        # Проверяем, что сервер вернул правильный ответ об ошибке
        assert response.status_code == 400
        assert b'User already exists' in response.data


def test_null_values(test_client):
    # Тест на пустые значения для обязательных полей
    response = test_client.post('/api/auth/register', data={
        'email': '',
        'password': '',
        'role': '',
        'first_name': '',
        'last_name': ''
    })
    assert response.status_code == 400
    assert b'Missing required fields' in response.data
