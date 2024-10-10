from sqlalchemy import Column, Integer, Enum, BLOB, String, TIMESTAMP, ForeignKey, Text
from sqlalchemy.orm import relationship

from Client_Api.extensions import db, current_timestamp



class Notification(db.Model):
    __tablename__ = 'notifications'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    content = Column(Text, nullable=False)
    sent_at = Column(TIMESTAMP, default=current_timestamp)

    user = relationship("User")
