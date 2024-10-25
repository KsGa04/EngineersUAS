from datetime import timezone, datetime, timedelta, date

from flask import Blueprint, request, jsonify
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from Models.user import User
from flask_jwt_extended import create_access_token
from Client_Server.app import db

auth_api = Blueprint('auth_api', __name__)


# Регистрация пользователя
@auth_api.route('/register', methods=['POST'])
def register():
    data = request.json

    # Извлекаем данные из запроса
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    is_employer = data.get('is_employer')  # Чекбокс работодатель
    university_name = data.get('university')  # Название университета
    group_name = data.get('group')  # Название группы

    # Хэшируем пароль для безопасного хранения
    hashed_password = generate_password_hash(password)

    # Регистрация пользователя
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hashed_password
    )
    db.session.add(user)
    db.session.flush()  # Генерирует id для пользователя перед добавлением других записей

    # Если пользователь - работодатель, сохраняем только его данные
    if is_employer:
        db.session.commit()
        return jsonify({"msg": "Employer registered successfully"}), 201

    # Для студентов добавляем также записи в таблицы `resume` и `educations`
    # Находим университет по названию
    university = University.query.filter_by(full_name=university_name).first()
    if not university:
        return jsonify({"msg": "University not found"}), 404

    # Находим группу по имени
    group = Group.query.filter_by(group_name=group_name).first()
    if not group:
        return jsonify({"msg": "Group not found"}), 404

    # Получаем направление по ID направления из группы
    direction_id = group.id_direction

    # Создаем запись в таблице `resume`
    resume = Resume(
        id_user=user.id_user,
        about_me=""
    )
    db.session.add(resume)
    db.session.flush()  # Генерирует id для резюме перед добавлением в таблицу `educations`

    # Создаем запись в таблице `educations`
    education = Education(
        id_resume=resume.id_resume,
        id_university=university.id_university,
        id_degree=1,  # Здесь предполагается степень, замените на подходящую
        id_direction=direction_id,
        group_number=group.id_group,
        start_date=date.today(),
        status="active"  # Установите статус по необходимости
    )
    db.session.add(education)

    # Сохраняем все изменения
    db.session.commit()

    return jsonify({"msg": "Student registered successfully"}), 201

# Авторизация пользователя
@auth_api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Проверка на отсутствие обязательных полей
    if not email or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    # Выполняем сырой SQL-запрос для получения данных о пользователе
    query = text("SELECT * FROM users WHERE email = :email")
    result = db.session.execute(query, {"email": email}).fetchone()

    if result is None:
        return jsonify({"msg": "Invalid credentials"}), 401

    # Явное преобразование результата в словарь
    user = {
        "email": result.email,
        "password": result.password,
        "role_id": result.role_id,
        "first_name": result.first_name,
        "last_name": result.last_name,
        "phone": result.phone,
        "created_at": result.created_at,
        "last_login": result.last_login
    }

    # Проверяем хеш пароля
    if not check_password_hash(user['password'], password):
        return jsonify({"msg": "Invalid credentials"}), 401

    # Создаем токен доступа, срок жизни токена 60 минут
    expires_in_minutes = 60
    access_token = create_access_token(identity=user['id'], expires_delta=timedelta(minutes=expires_in_minutes))

    db.session.commit()

    return jsonify(access_token=access_token), 200

