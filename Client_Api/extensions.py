from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from sqlalchemy.orm import declarative_base

# Инициализация расширений
db = SQLAlchemy()
jwt = JWTManager()

def current_timestamp():
    return datetime.now(timezone.utc)

