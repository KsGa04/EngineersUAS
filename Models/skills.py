from Client_Api.extensions import db


class Skill(db.Model):
    __tablename__ = 'skills'

    id_skill = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(100))
