from Client_Api.extensions import db


class Specifications(db.Model):
    __tablename__ = 'specifications'

    id_specifications = db.Column(db.Integer, primary_key=True)
    name_specifications = db.Column(db.String(255))