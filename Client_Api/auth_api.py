from datetime import timezone, datetime, timedelta

from flask import Blueprint, request, jsonify
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from Client_Api.extensions import db  # Импортируем db отсюда
from Models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_api = Blueprint('auth_api', __name__)


# Регистрация пользователя
@auth_api.route('/register', methods=['POST'])
def register():
    data = request.form.to_dict()  # Получаем данные формы
    email = data.get('email')
    password = data.get('password')
    role = data.get('role_rel.role_name')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone = data.get('phone')

    if not email or not password or not first_name or not last_name:
        return jsonify({'msg': 'Missing required fields'}), 400

    # Проверка существования пользователя с данным email
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 400

    # Обработка изображения, если оно было загружено
    image = None
    if 'image' in request.files:
        image = request.files['image'].read()  # Считываем изображение как байты

    # Хешируем пароль
    hashed_password = generate_password_hash(password)

    # Создаём нового пользователя
    new_user = User(
        email=email,
        password=hashed_password,
        role=role,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        image=image
    )

    # Добавляем и сохраняем пользователя в базе данных
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201


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
        "id": result.id,
        "email": result.email,
        "password": result.password,
        "role": result.role,
        "first_name": result.first_name,
        "last_name": result.last_name,
        "phone": result.phone,
        "telegram_username": result.telegram_username,
        "city": result.city,
        "image": result.image,
        "created_at": result.created_at,
        "updated_at": result.updated_at
    }

    # Проверяем хеш пароля
    if not check_password_hash(user['password'], password):
        return jsonify({"msg": "Invalid credentials"}), 401

    # Создаем токен доступа, срок жизни токена 60 минут
    expires_in_minutes = 60
    access_token = create_access_token(identity=user['id'], expires_delta=timedelta(minutes=expires_in_minutes))

    db.session.commit()

    return jsonify(access_token=access_token), 200



# Пример защищённого маршрута
@auth_api.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
