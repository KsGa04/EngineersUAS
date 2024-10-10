from sqlalchemy import Column, Integer, Enum, BLOB, String, TIMESTAMP, ForeignKey, Text
from sqlalchemy.orm import relationship

from Client_Api.extensions import db, current_timestamp


class Resume(db.Model):
    __tablename__ = 'resumes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    university_id = Column(Integer, ForeignKey('universities.id', ondelete='CASCADE'), nullable=False)
    specialty_id = Column(Integer, ForeignKey('specialties.id', ondelete='CASCADE'), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(255))
    summary = Column(Text)
    project_description = Column(Text)
    results = Column(Text)
    personal_projects = Column(Text)
    portfolio_links = Column(Text)
    created_at = Column(TIMESTAMP, default=current_timestamp)
    updated_at = Column(TIMESTAMP, default=current_timestamp, onupdate=current_timestamp)

    user = relationship("User")
    university = relationship("University")
    specialty = relationship("Specialty")
    group = relationship("Group")