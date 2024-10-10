from datetime import timedelta

from sqlalchemy import Column, Integer, Enum, BLOB, String, TIMESTAMP, ForeignKey, Text
from sqlalchemy.orm import relationship

from Client_Api.extensions import db, current_timestamp


class Session(db.Model):
    __tablename__ = 'sessions'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    token = Column(String(255), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, default=current_timestamp)
    deadline_at = Column(TIMESTAMP)

    user = relationship("User")

    def __init__(self, user_id, token, expires_in_minutes):
        self.user_id = user_id
        self.token = token
        self.created_at = current_timestamp
        self.ended_at = self.created_at + timedelta(minutes=expires_in_minutes)
