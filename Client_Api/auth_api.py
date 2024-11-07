from datetime import timezone, datetime, timedelta, date

from flask import Blueprint, request, jsonify, make_response
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash

from Models import University, Group, Resume, Education
from Models.user import User
from flask_jwt_extended import create_access_token, set_access_cookies
from Client_Api.extensions import db

auth_api = Blueprint('auth_api', __name__)


# Регистрация пользователя
@auth_api.route('/register', methods=['POST'])
def register():
    data = request.json

    required_fields = ['email', 'password', 'first_name', 'last_name', 'middle_name', 'role_id']
    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"{field} is required"}), 400

    email = data['email']
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']
    middle_name = data['middle_name']
    role_id = data['role_id']

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User with this email already exists"}), 409

    if len(password) < 8:
        return jsonify({"msg": "Password must be at least 8 characters long"}), 400

    # Хэшируем пароль перед сохранением
    hashed_password = generate_password_hash(password)

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hashed_password,
        middle_name=middle_name,
        role_id=role_id# Сохраняем хэшированный пароль
    )
    db.session.add(user)
    db.session.flush()  # Генерирует id для пользователя

    resume = Resume(id_user=user.id_user, about_me="", id_pattern=1)
    db.session.add(resume)
    db.session.flush()

    db.session.commit()

    return jsonify({"msg": "Student registered successfully"}), 201


@auth_api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role_id = data.get('role_id')

    user = User.query.filter_by(email=email).first()
    bools = check_password_hash(user.password, password)
    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Неверные учетные данные"}), 401

    # Генерация токена
    authToken = create_access_token(identity=user.id_user, additional_claims={"role_id": user.role_id, "id_resume": user.id_user})
    resume = Resume.query.filter_by(id_user=user.id_user).first()

    # Настройка ответа с cookies
    response = make_response(jsonify({"user_id": user.id_user, "role_id": user.role_id, "id_pattern": resume.id_pattern if resume else None}))
    set_access_cookies(response, authToken)

    return response, 200