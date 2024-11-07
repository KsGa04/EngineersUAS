from datetime import timedelta

import pytest
from flask_jwt_extended import decode_token
from werkzeug.security import generate_password_hash
from Client_Api.extensions import db
from Models.user import User


@pytest.fixture(scope='module')
def test_client():
    from app import app
    from config import Config
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

def test_successful_login(test_client, init_database):
    response = test_client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data

    # Проверка токена в базе данных
    token = data['access_token']
    decoded_token = decode_token(token)
    assert 'sub' in decoded_token  # Проверка того, что токен содержит идентификатор пользователя


# Тест на неудачную авторизацию (неверный пароль)
def test_invalid_credentials(test_client, init_database):
    response = test_client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert b'Invalid credentials' in response.data

# Тест на отсутствие email или пароля
def test_missing_email_or_password(test_client):
    # Без email
    response = test_client.post('/api/auth/login', json={
        'password': 'password123'
    })
    assert response.status_code == 400
    assert b'Missing required fields' in response.data

    # Без пароля
    response = test_client.post('/api/auth/login', json={
        'email': 'test@example.com'
    })
    assert response.status_code == 400
    assert b'Missing required fields' in response.data

# Тест на проверку истечения срока действия токена
def test_token_expiry(test_client, init_database):
    # Создаем токен с очень коротким сроком действия (1 секунда)
    test_client.application.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=1)

    response = test_client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    data = response.get_json()
    token = data['access_token']

    # Ждем истечения срока действия токена
    import time
    time.sleep(2)

    # Попытка использовать истекший токен
    protected_response = test_client.get('/api/protected', headers={
        'Authorization': f'Bearer {token}'
    })
    assert protected_response.status_code == 401
    assert b'Token has expired' in protected_response.data
