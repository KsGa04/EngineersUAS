from Client_Api.extensions import db


class Work(db.Model):
    __tablename__ = 'work'

    id_work = db.Column(db.Integer, primary_key=True)
    id_resume = db.Column(db.Integer, db.ForeignKey('resume.id_resume'), nullable=False)
    position = db.Column(db.String(255))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    # Связь с резюме
    resume = db.relationship('Resume', back_populates='works')

    # Связь с организацией через WorkOrganization
    organizations = db.relationship('Organization', secondary='work_organization', backref='works')
