from datetime import timezone, datetime, timedelta, date

from flask import Blueprint, request, jsonify, make_response, url_for, flash, redirect, render_template
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash

from Models import University, Group, Resume, Education, UserSocialNetwork
from Models.user import User
from flask_jwt_extended import create_access_token, set_access_cookies
from Client_Api.extensions import db, send_reset_email, serializer

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
    tg = data.get('tg')  # Optional field
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
    email = data.get('email')
    password = data.get('password')
    role_id = data.get('role_id')

    user = User.query.filter_by(email=email).first()
    bools = check_password_hash(user.password, password)
    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Неверные учетные данные"}), 401

    # Генерация токена
    authToken = create_access_token(identity=user.id_user, additional_claims={"role_id": user.role_id, "id_resume": user.id_user, "login":email, "password": password,})
    resume = Resume.query.filter_by(id_user=user.id_user).first()

    # Настройка ответа с cookies
    response = make_response(jsonify({"user_id": user.id_user,"login":email, "password": password, "role_id": user.role_id, "id_resume": resume.id_resume, "id_pattern": resume.id_pattern if resume else None, "token": authToken}))
    set_access_cookies(response, authToken)

    return response, 200


@auth_api.route('/passwordrecovery', methods=['POST'])
def password_recovery():
    email = request.json.get('email')
    user = User.query.filter_by(email=email).first_or_404()

    token = serializer.dumps(email, salt="password-recovery")
    reset_link = url_for('auth_api.reset_password', token=token, _external=True)

    send_reset_email(email, reset_link)
    return jsonify({"msg": f"Password reset link sent to {email}"}), 200


@auth_api.route('/resetpassword/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:    
        email = serializer.loads(token, salt="password-recovery", max_age=3600)
    except Exception as e:
        flash("Invalid or expired token", "danger")
        return redirect(url_for('auth_api.login'))

    user = User.query.filter_by(email=email).first()

    if request.method == 'POST':
        new_password = request.form.get('password')
        if not new_password:
            flash("Password is required", "danger")
            return render_template('reset_password.html')

        user.password = generate_password_hash(new_password)
        db.session.commit()

        flash("Password reset successfully", "success")
        return redirect(url_for('auth_api.login'))

    return render_template('reset_password.html')