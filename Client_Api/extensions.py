from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Инициализация расширений
db = SQLAlchemy()
jwt = JWTManager()
