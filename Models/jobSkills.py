from Client_Api.extensions import db


class JobSkills(db.Model):
    __tablename__ = 'job_skills'

    id = db.Column(db.Integer, primary_key=True)  # Искусственный первичный ключ
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'))

    # Связи
    job = db.relationship('Job', backref=db.backref('job_skills', cascade="all, delete-orphan"))
    skill = db.relationship('Skill', backref=db.backref('job_skills', cascade="all, delete-orphan"))
