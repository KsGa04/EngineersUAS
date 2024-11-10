from Client_Api.extensions import db


class UserSocialNetwork(db.Model):
    __tablename__ = 'user_social_networks'

    id_user_social_network = db.Column(db.Integer, primary_key=True)
    id_resume = db.Column(db.Integer, db.ForeignKey('resume.id_resume'), nullable=False)
    network_link = db.Column(db.String(255), nullable=False)
