from sqlalchemy import Column, Integer, Enum, BLOB, String, TIMESTAMP

from Client_Api.extensions import db, current_timestamp


class Skill(db.Model):
    __tablename__ = 'skills'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=current_timestamp)