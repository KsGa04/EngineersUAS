from sqlalchemy.testing import db


class Skills(db.Model):
    __tablename__ = 'skills'
    id_skill = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(100))