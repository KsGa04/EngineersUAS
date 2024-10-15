from sqlalchemy.testing import db


class Projects(db.Model):
    __tablename__ = 'projects'
    id_project = db.Column(db.Integer, primary_key=True)
    id_resume = db.Column(db.Integer, db.ForeignKey('resume.id_resume', ondelete='CASCADE'))
    project_name = db.Column(db.String(255))
    project_description = db.Column(db.Text)
    technologies_used = db.Column(db.String(255))
    project_link = db.Column(db.String(255))

    resume_rel = db.relationship('Resume', backref='projects')