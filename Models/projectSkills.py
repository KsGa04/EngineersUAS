from sqlalchemy.testing import db


class ProjectSkills(db.Model):
    __tablename__ = 'project_skills'
    id = db.Column(db.Integer, primary_key=True)
    id_project = db.Column(db.Integer, db.ForeignKey('projects.id_project'))
    id_skill = db.Column(db.Integer, db.ForeignKey('skills.id_skill'))