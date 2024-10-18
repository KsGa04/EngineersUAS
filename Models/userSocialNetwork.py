from Client_Api.extensions import db


class UserSocialNetwork(db.Model):
    __tablename__ = 'user_social_networks'

    id_user_social_network = db.Column(db.Integer, primary_key=True)
    id_resume = db.Column(db.Integer, db.ForeignKey('resume.id_resume'), nullable=False)
    id_social_network_type = db.Column(db.Integer, db.ForeignKey('social_network_types.id_social_network_type'),
                                       nullable=False)
    network_link = db.Column(db.String(255), nullable=False)
