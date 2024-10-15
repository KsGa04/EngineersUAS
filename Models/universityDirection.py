from sqlalchemy.testing import db


class UniversityDirection(db.Model):
    __tablename__ = 'university_direction'
    id = db.Column(db.Integer, primary_key=True)
    id_university = db.Column(db.Integer, db.ForeignKey('university.id_university'))
    id_direction = db.Column(db.Integer, db.ForeignKey('direction.id_direction'))