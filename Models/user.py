from Client_Api.extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id_user = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    middle_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(255), nullable=False)
    birth_date = db.Column(db.Date)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id_role'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_login = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    profile_photo = db.Column(db.LargeBinary)
    address = db.Column(db.String(255))

    resumes = db.relationship('Resume', backref='user')
