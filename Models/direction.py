from Client_Api.extensions import db


class Direction(db.Model):
    __tablename__ = 'direction'
    id_direction = db.Column(db.Integer, primary_key=True)
    direction_code = db.Column(db.String(50))
    direction_name = db.Column(db.String(255))