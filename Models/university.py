from Client_Api.extensions import db


class University(db.Model):
    __tablename__ = 'university'
    id_university = db.Column(db.Integer, primary_key=True)
    short_name = db.Column(db.String(100))
    full_name = db.Column(db.String(255))
    location = db.Column(db.String(255))
    website = db.Column(db.String(255))
    contact_info = db.Column(db.String(255))