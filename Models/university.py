from sqlalchemy import Column, Integer, Enum, BLOB, String, TIMESTAMP, ForeignKey, Text
from sqlalchemy.orm import relationship

from Client_Api.extensions import db, current_timestamp


class University(db.Model):
    __tablename__ = 'universities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=current_timestamp)
    updated_at = Column(TIMESTAMP, default=current_timestamp, onupdate=current_timestamp)