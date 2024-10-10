from sqlalchemy import Column, Integer, Enum, BLOB, String, TIMESTAMP, ForeignKey, Text
from sqlalchemy.orm import relationship

from Client_Api.extensions import db, current_timestamp

class Group(db.Model):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_number = Column(String(50), nullable=False)
    specialty_id = Column(Integer, ForeignKey('specialties.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP, default=current_timestamp)
    updated_at = Column(TIMESTAMP, default=current_timestamp, onupdate=current_timestamp)

    specialty = relationship("Specialty")