from sqlalchemy import Column, Integer, Enum, BLOB, String, TIMESTAMP, ForeignKey, Text
from sqlalchemy.orm import relationship

from Client_Api.extensions import db, current_timestamp


class ResumeSkill(db.Model):
    __tablename__ = 'resume_skills'

    id = Column(Integer, primary_key=True, autoincrement=True)
    resume_id = Column(Integer, ForeignKey('resumes.id', ondelete='CASCADE'), nullable=False)
    skill_id = Column(Integer, ForeignKey('skills.id', ondelete='CASCADE'), nullable=False)

    resume = relationship("Resume")
    skill = relationship("Skill")