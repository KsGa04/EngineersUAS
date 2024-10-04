from datetime import datetime, timezone

from Client_Api.extensions import db


class Resume(db.Model):
    __tablename__ = 'resumes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255))
    summary = db.Column(db.Text)
    education = db.Column(db.String(255))
    group_number = db.Column(db.String(50))
    fpv_experience = db.Column(db.Text)
    programming_languages = db.Column(db.Text)
    radiophysics_knowledge = db.Column(db.Text)
    circuitry_knowledge = db.Column(db.Text)
    three_d_modeling_experience = db.Column(db.Text)
    controllers_experience = db.Column(db.Text)
    composite_materials_experience = db.Column(db.Text)
    management_skills = db.Column(db.Text)
    other_skills = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Связи
    skills = db.relationship('Skill', secondary='resume_skills', lazy='subquery',
                             backref=db.backref('resumes', lazy=True))
    job_applications = db.relationship('JobApplication', backref='resume', cascade="all, delete-orphan", lazy=True)
    languages = db.relationship('Language', secondary='language_resume', lazy='subquery',
                                backref=db.backref('resumes', lazy=True))
