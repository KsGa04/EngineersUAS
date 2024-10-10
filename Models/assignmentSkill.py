from sqlalchemy import Column, Integer, Enum, BLOB, String, TIMESTAMP, ForeignKey, Text
from sqlalchemy.orm import relationship

from Client_Api.extensions import db, current_timestamp

class AssignmentSkill(db.Model):
    __tablename__ = 'assignment_skills'

    id = Column(Integer, primary_key=True, autoincrement=True)
    assignment_id = Column(Integer, ForeignKey('assignments.id', ondelete='CASCADE'), nullable=False)
    skill_id = Column(Integer, ForeignKey('skills.id', ondelete='CASCADE'), nullable=False)

    assignment = relationship("Assignment")
    skill = relationship("Skill")