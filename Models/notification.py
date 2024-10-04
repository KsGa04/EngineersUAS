from Client_Api.extensions import db


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Искусственный первичный ключ
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Переименовываем 'user' на 'notification_user'
    user = db.relationship('User', backref=db.backref('user', cascade="all, delete-orphan"))
