from Client_Api.extensions import db


class Organization(db.Model):
    __tablename__ = 'organization'

    id_organization = db.Column(db.Integer, primary_key=True)
    organization_name = db.Column(db.String(255))
    location = db.Column(db.String(255))
    website = db.Column(db.String(255))
