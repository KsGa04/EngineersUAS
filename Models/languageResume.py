from sqlalchemy import Column, Integer, Enum, BLOB, String, TIMESTAMP, ForeignKey, Text
from sqlalchemy.orm import relationship

from Client_Api.extensions import db, current_timestamp


class ResumeLanguage(db.Model):
    __tablename__ = 'resume_languages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    resume_id = Column(Integer, ForeignKey('resumes.id', ondelete='CASCADE'), nullable=False)
    language_id = Column(Integer, ForeignKey('languages.id', ondelete='CASCADE'), nullable=False)
    proficiency_level = Column(Enum('beginner', 'intermediate', 'advanced', 'fluent'), nullable=False)

    resume = relationship("Resume")
    language = relationship("Language")