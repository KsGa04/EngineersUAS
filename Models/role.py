from Client_Api.extensions import db


class Roles(db.Model):
    __tablename__ = 'roles'
    id_role = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(100), nullable=False)