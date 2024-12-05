from datetime import timezone, datetime, timedelta, date

from flask import Blueprint, request, jsonify, make_response
from sqlalchemy import text, or_
from werkzeug.security import generate_password_hash, check_password_hash

from Models import University, Group, Resume, Education, UserSocialNetwork
from Models.user import User
from flask_jwt_extended import create_access_token, set_access_cookies
from Client_Api.extensions import db

auth_api = Blueprint('auth_api', __name__)


# Регистрация пользователя
@auth_api.route('/register', methods=['POST'])
def register():
    data = request.json

    required_fields = ['email', 'password', 'first_name', 'last_name', 'phone', 'role_id']
    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"{field} is required"}), 400

    email = data['email']
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']
    tg = data.get('tg')  # Optional field
    phone = data.get('phone')  # Optional
    role_id = data['role_id']

    if User.query.filter_by(email=email).first() or User.query.filter_by(phone=phone).first():
        return jsonify({"msg": "Пользователь с данным email уже существует"}), 409

    if len(password) < 8:
        return jsonify({"msg": "Пароль должен состоять минимум из 8 символов"}), 400

    # Хэшируем пароль перед сохранением
    hashed_password = generate_password_hash(password)

    if phone:
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            role_id=role_id,
            phone=phone,
        )
    else:
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            role_id=role_id
        )
    db.session.add(user)
    db.session.flush()  # Генерирует id для пользователя

    resume = Resume(id_user=user.id_user, about_me="", id_pattern=1)
    db.session.add(resume)
    db.session.flush()

    # Обработка и добавление Telegram ссылки
    if tg:
        # Нормализация TG-ссылки
        if tg.startswith('@'):
            tg = tg[1:]  # Убираем символ @
        if not tg.startswith('https://t.me/'):
            tg = f'https://t.me/{tg}'

        user_social_network = UserSocialNetwork(
            id_resume=resume.id_resume,
            network_link=tg
        )
        db.session.add(user_social_network)

    db.session.commit()

    return jsonify({"msg": "Студент успешно зарегистрирован"}), 201



@auth_api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    emailOrphone = data.get('email')
    password = data.get('password')

    # Поиск пользователя
    user = User.query.filter(or_(User.email == emailOrphone, User.phone == emailOrphone)).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Неверные учетные данные"}), 401

    # Генерация токена
    try:
        authToken = create_access_token(
            identity=str(user.id_user),  # Преобразуем ID в строку
            additional_claims={
                "role_id": user.role_id,
                "id_resume": str(user.id_user),  # Преобразуем в строку, если это число
                "login": user.email
            }
        )
    except Exception as e:
        print(f"Ошибка генерации токена: {str(e)}")
        return jsonify({"msg": "Ошибка авторизации."}), 500

    resume = Resume.query.filter_by(id_user=user.id_user).first()

    # Формирование ответа
    response_data = {
        "user_id": user.id_user,
        "login": user.email,
        "role_id": user.role_id,
        "id_resume": resume.id_resume if resume else None,
        "id_pattern": resume.id_pattern if resume else None,
        "token": authToken
    }

    try:
        response = make_response(jsonify(response_data))
        set_access_cookies(response, authToken)
    except Exception as e:
        print(f"Ошибка при установке cookies: {str(e)}")
        return jsonify({"msg": "Ошибка при установке cookies"}), 500

    return response, 200

