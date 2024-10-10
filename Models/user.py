from datetime import datetime, timezone

from sqlalchemy import Column, Integer, Enum, BLOB, String, TIMESTAMP

from Client_Api.extensions import db, current_timestamp


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum('student', 'employer', 'UEM', 'admin'), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    telegram_username = Column(String(50))
    city = Column(String(255))
    image = Column(BLOB)
    created_at = Column(TIMESTAMP, default=current_timestamp)
    updated_at = Column(TIMESTAMP, default=current_timestamp, onupdate=current_timestamp)
