from sqlalchemy import Column, Integer, Enum, BLOB, String, TIMESTAMP, ForeignKey, Text
from sqlalchemy.orm import relationship

from Client_Api.extensions import db, current_timestamp

class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)
    type = Column(Enum('lab', 'coursework', 'diploma'), nullable=False)
    created_at = Column(TIMESTAMP, default=current_timestamp)
    updated_at = Column(TIMESTAMP, default=current_timestamp, onupdate=current_timestamp)

    group = relationship("Group")