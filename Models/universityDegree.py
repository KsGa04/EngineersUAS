from Client_Api.extensions import db


class UniversityDegree(db.Model):
    __tablename__ = 'university_degree'

    id = db.Column(db.Integer, primary_key=True)
    id_university = db.Column(db.Integer, db.ForeignKey('university.id_university'), nullable=False)
    id_degree = db.Column(db.Integer, db.ForeignKey('degree.id_degree'), nullable=False)

    university = db.relationship('University', backref='degrees')
    degree = db.relationship('Degree', backref='universities')
