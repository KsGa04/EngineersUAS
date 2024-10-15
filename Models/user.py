from sqlalchemy.testing import db


class User(db.Model):
    __tablename__ = 'user'
    id_user = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    middle_name = db.Column(db.String(255))
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(255), nullable=False)
    birth_date = db.Column(db.Date)
    role = db.Column(db.Integer, db.ForeignKey('roles.id_role', ondelete='SET NULL'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_login = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    account_status = db.Column(db.String(50))
    profile_photo = db.Column(db.String(255))
    address = db.Column(db.String(255))

    role_rel = db.relationship('Roles', backref='users')