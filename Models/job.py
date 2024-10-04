from datetime import datetime, timezone

from Client_Api.extensions import db


class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    requirements = db.Column(db.Text)
    location = db.Column(db.String(255))
    salary_range = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # # Связи
    # skills = db.relationship('Skill', secondary='job_skills', lazy='subquery',
    #                          backref=db.backref('jobs', lazy=True))
    # job_applications = db.relationship('JobApplication', backref='job', cascade="all, delete-orphan", lazy=True)
