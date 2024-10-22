from Client_Api.extensions import db


class Projects(db.Model):
    __tablename__ = 'projects'

    id_project = db.Column(db.Integer, primary_key=True)
    id_resume = db.Column(db.Integer, db.ForeignKey('resume.id_resume'), nullable=False)
    project_name = db.Column(db.String(255))
    project_description = db.Column(db.Text)
    project_link = db.Column(db.String(255))
