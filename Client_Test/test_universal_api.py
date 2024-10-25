import pytest
from flask import Flask

from Client_Api.extensions import db
from Client_Server.app import app
from Client_Server.config import TestingConfig
# Подключите ваше приложение и базу данных
from Models import Role, User, Resume  # Импортируйте необходимые модели


@pytest.fixture(scope='module')
def test_client():
    # Применяем тестовую конфигурацию
    app.config.from_object(TestingConfig)  # Подключаем тестовый конфиг

    # Создаем тестовый клиент
    with app.test_client() as testing_client:
        with app.app_context():
            # Инициализация базы данных для тестов
            db.create_all()  # Создаем все таблицы
            yield testing_client  # Тесты выполняются здесь
            db.session.remove()
            db.drop_all()  # Удаляем все таблицы после теста


@pytest.fixture
def add_test_data():
    # Добавляем тестовые данные
    def _add_test_data():
        role = Role(role_name="Student")
        user = User(first_name="John", last_name="Doe", email="john.doe@example.com", password="hashed_password")
        resume = Resume(id_user=user.id_user, about_me="Test resume")

        db.session.add(role)
        db.session.add(user)
        db.session.add(resume)
        db.session.commit()

    return _add_test_data


# Тест для получения всех записей из таблицы 'roles'
def test_get_roles(test_client, add_test_data):
    add_test_data()
    response = test_client.get('/api/roles')
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) > 0
    assert json_data[0]['role_name'] == 'Student'


def test_get_users(test_client, add_test_data):
    add_test_data()
    response = test_client.get('/api/users')
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) > 0
    assert json_data[0]['first_name'] == 'John'
    assert json_data[0]['last_name'] == 'Doe'


# Тест для получения данных по резюме
def test_get_resumes(test_client):
    # Отправляем GET запрос к универсальному API для таблицы 'resume'
    response = test_client.get('/api/resume')

    # Проверяем успешный статус
    assert response.status_code == 200

    # Проверяем содержимое
    json_data = response.get_json()
    assert len(json_data) > 0
    assert json_data[1]['about_me'] == 'Test resume'


# Тест для ошибки: Неверная таблица
def test_invalid_table(test_client):
    # Отправляем GET запрос к несуществующей таблице
    response = test_client.get('/api/nonexistent_table')

    # Ожидаем код ответа 400
    assert response.status_code == 400
    json_data = response.get_json()
    assert "Table nonexistent_table does not exist" in json_data["msg"]
