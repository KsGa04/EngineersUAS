from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from sqlalchemy.orm import declarative_base
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

# Инициализация расширений
db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()
serializer = URLSafeTimedSerializer('your_secret_key')

def current_timestamp():
    return datetime.now(timezone.utc)


def send_reset_email(email, reset_link):
    msg = Message(
        subject="Сброс пароля",
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[email]
    )
    msg.body = f"Перейдите по ссылке чтобы поменять пароль: {reset_link}"
    msg.html = f"<p>Перейдите по ссылке чтобы поменять пароль:</p><a href='{reset_link}'>Сброс пароля</a>"
    mail.send(msg)