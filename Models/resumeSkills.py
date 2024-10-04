from Client_Api.extensions import db


from Client_Api.extensions import db

class ResumeSkills(db.Model):
    __tablename__ = 'resume_skills'

    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), primary_key=True)

    # Дополнительно можно добавить связь, если это нужно
    resume = db.relationship('Resume', backref=db.backref('resume_skills', cascade="all, delete-orphan"))
    skill = db.relationship('Skill', backref=db.backref('resume_skills', cascade="all, delete-orphan"))
