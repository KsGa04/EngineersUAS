import pytest
from Client_Api.extensions import db
from config import TestingConfig
from Models import Role, User, Resume
from app import create_app

app = create_app(TestingConfig)


@pytest.fixture(scope="module")
def test_client():
    with app.test_client() as client:
        yield client


def setup_module(module):
    role = Role(role_name="Student")
    user = User(id_user=1, first_name="John", last_name="Doe", email="john.doe@example.com", password="hashed_password")
    resume = Resume(id_user=user.id_user, about_me="Test resume")
    with app.app_context():
        db.create_all()
        db.session.add(role)
        db.session.add(user)
        db.session.add(resume)
        db.session.commit()


def teardown_module(module):
    with app.app_context():
        db.session.remove()
        db.drop_all()


# Тест для получения всех записей из таблицы 'role'
def test_get_roles(test_client):
    response = test_client.get('/api/role')
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) > 0
    assert json_data[0]['role_name'] == 'Student'


# Тест для получения всех записей из таблицы 'user'
def test_get_users(test_client):
    response = test_client.get('/api/user')
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
    assert json_data[0]['about_me'] == 'Test resume'


# Тест для ошибки: Неверная таблица
def test_invalid_table(test_client):
    # Отправляем GET запрос к несуществующей таблице
    response = test_client.get('/api/nonexistent_table')

    # Ожидаем код ответа 400
    assert response.status_code == 400
    json_data = response.get_json()
    assert "Table nonexistent_table does not exist" in json_data["msg"]
