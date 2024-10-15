from sqlalchemy.testing import db


class ResumeSkills(db.Model):
    __tablename__ = 'resume_skills'
    id = db.Column(db.Integer, primary_key=True)
    id_resume = db.Column(db.Integer, db.ForeignKey('resume.id_resume'))
    id_skill = db.Column(db.Integer, db.ForeignKey('skills.id_skill'))