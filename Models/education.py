from sqlalchemy.testing import db


class Education(db.Model):
    __tablename__ = 'education'
    id_education = db.Column(db.Integer, primary_key=True)
    id_resume = db.Column(db.Integer, db.ForeignKey('resume.id_resume', ondelete='CASCADE'))
    id_university = db.Column(db.Integer, db.ForeignKey('university.id_university'))
    id_direction = db.Column(db.Integer, db.ForeignKey('direction.id_direction'))
    group = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(50))

    resume_rel = db.relationship('Resume', backref='education')