from flask import Blueprint, request, jsonify
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
    role = data.get('role')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone = data.get('phone')
    telegram_username = data.get('telegram_username')
    city = data.get('city')

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
        telegram_username=telegram_username,
        city=city,
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

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)


# Пример защищённого маршрута
@auth_api.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
