import pytest

from Client_Api.extensions import db
from app import app
from Models import University, Group



"""
Нужно протестировать чтобы работало на тестовой конфигурации
"""
@pytest.fixture(scope='module')
def test_client():
    app.config.from_object('config.TestingConfig')  # Подключаем тестовую конфигурацию
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.session.remove()
            db.drop_all()

@pytest.fixture
def add_university_and_group():
    # Добавляем тестовый университет и группу для регистрации студентов
    def _add_university_and_group():
        university = University(full_name="Test University")
        group = Group(group_name="Test Group", start_year=2020, id_university=university.id_university, id_direction=1)
        db.session.add(university)
        db.session.add(group)
        db.session.commit()
    return _add_university_and_group

def test_register_employer(test_client):
    # Тест успешной регистрации работодателя
    response = test_client.post('/register', json={
        "email": "employer@example.com",
        "password": "securePassword123",
        "first_name": "EmployerFirst",
        "last_name": "EmployerLast",
        "is_employer": True
    })
    assert response.status_code == 201
    assert response.get_json()["msg"] == "Employer registered successfully"

def test_register_student(test_client, add_university_and_group):
    # Добавляем университет и группу для регистрации студента
    add_university_and_group()
    response = test_client.post('/register', json={
        "email": "student@example.com",
        "password": "securePassword123",
        "first_name": "StudentFirst",
        "last_name": "StudentLast",
        "is_employer": False,
        "university": "Test University",
        "group": "Test Group"
    })
    assert response.status_code == 201
    assert response.get_json()["msg"] == "Student registered successfully"

def test_register_existing_email(test_client, add_university_and_group):
    # Проверка ошибки при повторной регистрации с тем же email
    add_university_and_group()
    test_client.post('/register', json={
        "email": "duplicate@example.com",
        "password": "securePassword123",
        "first_name": "UserFirst",
        "last_name": "UserLast",
        "is_employer": True
    })
    # Повторная регистрация с тем же email
    response = test_client.post('/register', json={
        "email": "duplicate@example.com",
        "password": "anotherPassword123",
        "first_name": "UserFirst",
        "last_name": "UserLast",
        "is_employer": True
    })
    assert response.status_code == 409
    assert response.get_json()["msg"] == "User with this email already exists"

def test_register_student_without_university(test_client):
    # Проверка ошибки при отсутствии университета и группы у студента
    response = test_client.post('/auth/register', json={
        "email": "newstudent@example.com",
        "password": "securePassword123",
        "first_name": "NewStudentFirst",
        "last_name": "NewStudentLast",
        "is_employer": False
    })
    assert response.status_code == 400
    assert response.get_json()["msg"] == "University and group are required for student registration"

