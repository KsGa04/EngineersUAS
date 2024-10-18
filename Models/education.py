from Client_Api.extensions import db


class Education(db.Model):
    __tablename__ = 'educations'

    id_education = db.Column(db.Integer, primary_key=True)
    id_resume = db.Column(db.Integer, db.ForeignKey('resume.id_resume'), nullable=False)
    id_university = db.Column(db.Integer, db.ForeignKey('university.id_university'), nullable=False)
    id_degree = db.Column(db.Integer, db.ForeignKey('degree.id_degree'), nullable=False)
    id_direction = db.Column(db.Integer, db.ForeignKey('direction.id_direction'), nullable=False)
    group_number = db.Column(db.Integer, db.ForeignKey('groups_number.id_group'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(50))

    degree = db.relationship('Degree', backref='educations')

    # Связь с моделью University
    university = db.relationship('University', backref='educations')

    # Связь с моделью Direction
    direction = db.relationship('Direction', backref='educations')
