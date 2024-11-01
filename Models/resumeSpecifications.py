from Client_Api.extensions import db


class ResumeSpecifications(db.Model):
    __tablename__ = 'resume_specifications'

    id_resume_specifications = db.Column(db.Integer, primary_key=True)
    id_specifications = db.Column(db.Integer, db.ForeignKey('specifications.id_specifications'), nullable=False)
    id_resume = db.Column(db.Integer, db.ForeignKey('resume.id_resume'), nullable=False)
