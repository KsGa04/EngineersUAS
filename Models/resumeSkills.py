from Client_Api.extensions import db


class ResumeSkill(db.Model):
    __tablename__ = 'resume_skills'

    id_resume_skills = db.Column(db.Integer, primary_key=True)
    id_resume = db.Column(db.Integer, db.ForeignKey('resume.id_resume'), nullable=False)
    id_skill = db.Column(db.Integer, db.ForeignKey('skills.id_skill'), nullable=False)
