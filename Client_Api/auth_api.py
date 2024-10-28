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

    # Проверка обязательных полей
    required_fields = ['email', 'password', 'first_name', 'last_name', 'is_employer']
    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"{field} is required"}), 400

    email = data['email']
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']
    is_employer = data['is_employer']
    university_name = data.get('university')  # Учитываем, если поле отсутствует
    group_name = data.get('group')

    # Проверка уникальности email
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User with this email already exists"}), 409

    # Проверка длины пароля
    if len(password) < 8:
        return jsonify({"msg": "Password must be at least 8 characters long"}), 400

    # Хэшируем пароль
    hashed_password = generate_password_hash(password)

    # Создание пользователя
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hashed_password
    )
    db.session.add(user)
    db.session.flush()  # Генерирует id для пользователя

    if is_employer:
        db.session.commit()
        return jsonify({"msg": "Employer registered successfully"}), 201

    # Проверка дополнительных полей для студентов
    if not university_name or not group_name:
        return jsonify({"msg": "University and group are required for student registration"}), 400

    # Находим университет по названию
    university = University.query.filter_by(full_name=university_name).first()
    if not university:
        return jsonify({"msg": "University not found"}), 404

    # Находим группу по имени
    group = Group.query.filter_by(group_name=group_name).first()
    if not group:
        return jsonify({"msg": "Group not found"}), 404

    # Получаем направление
    direction_id = group.id_direction

    # Создаем запись в таблице `resume`
    resume = Resume(id_user=user.id_user, about_me="")
    db.session.add(resume)
    db.session.flush()  # Генерирует id для резюме

    # Создаем запись в таблице `educations`
    education = Education(
        id_resume=resume.id_resume,
        id_university=university.id_university,
        id_degree=1,  # Предположим, что id_degree передан правильно
        id_direction=direction_id,
        group_number=group.id_group,
        start_date=date.today(),
        status="active"
    )
    db.session.add(education)

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
    return jsonify({"msg": "Успешная авторизация"}), 200
