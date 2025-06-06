from Client_Api.extensions import db


class UniversityDirection(db.Model):
    __tablename__ = 'university_direction'

    id_university_direction = db.Column(db.Integer, primary_key=True)
    id_university = db.Column(db.Integer, db.ForeignKey('university.id_university'), nullable=False)
    id_direction = db.Column(db.Integer, db.ForeignKey('direction.id_direction'), nullable=False)
