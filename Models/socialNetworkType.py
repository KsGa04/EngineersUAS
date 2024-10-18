from Client_Api.extensions import db


class SocialNetworkType(db.Model):
    __tablename__ = 'social_network_types'

    id_social_network_type = db.Column(db.Integer, primary_key=True)
    network_name = db.Column(db.String(100), unique=True, nullable=False)
