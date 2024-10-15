from Client_Api.extensions import db


class WorkExperience(db.Model):
    __tablename__ = 'work_experience'
    id_experience = db.Column(db.Integer, primary_key=True)
    id_resume = db.Column(db.Integer, db.ForeignKey('resume.id_resume', ondelete='CASCADE'))
    company_name = db.Column(db.String(255))
    position = db.Column(db.String(255))
    work_period = db.Column(db.Date)
    responsibilities = db.Column(db.Text)

    resume_rel = db.relationship('Resume', backref='work_experience')