from sqlalchemy import Column, Integer, Enum, BLOB, String, TIMESTAMP, ForeignKey, Text
from sqlalchemy.orm import relationship

from Client_Api.extensions import db, current_timestamp


class JobApplication(db.Model):
    __tablename__ = 'job_applications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id', ondelete='CASCADE'), nullable=False)
    resume_id = Column(Integer, ForeignKey('resumes.id', ondelete='CASCADE'), nullable=False)
    status = Column(Enum('pending', 'reviewed', 'accepted', 'rejected'), default='pending')
    applied_at = Column(TIMESTAMP, default=current_timestamp)

    user = relationship("User")
    job = relationship("Job")
    resume = relationship("Resume")
