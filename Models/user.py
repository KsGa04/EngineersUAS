from datetime import datetime, timezone

from Client_Api.extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('student', 'employer', 'admin'), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    telegram_username = db.Column(db.String(50))
    city = db.Column(db.String(255))
    image = db.Column(db.LargeBinary)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Связь с резюме
    resumes = db.relationship('Resume', backref='user', cascade="all, delete-orphan", lazy=True)

    # Остальные связи
    jobs = db.relationship('Job', backref='employer', cascade="all, delete-orphan", lazy=True)
    job_applications = db.relationship('JobApplication', backref='user', cascade="all, delete-orphan", lazy=True)
    sessions = db.relationship('Session', backref='user', cascade="all, delete-orphan", lazy=True)
