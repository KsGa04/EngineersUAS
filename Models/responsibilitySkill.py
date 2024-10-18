from Client_Api.extensions import db


class ResponsibilitySkill(db.Model):
    __tablename__ = 'responsibility_skills'

    id = db.Column(db.Integer, primary_key=True)
    id_responsibility = db.Column(db.Integer, db.ForeignKey('responsibilities.id_responsibility'), nullable=False)
    id_skill = db.Column(db.Integer, db.ForeignKey('skills.id_skill'), nullable=False)
