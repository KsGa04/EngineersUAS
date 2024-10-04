from datetime import datetime, timezone

from Client_Api.extensions import db


class Session(db.Model):
    __tablename__ = 'sessions'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    ended_at = db.Column(db.DateTime)
