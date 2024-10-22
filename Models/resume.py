from Client_Api.extensions import db


class Resume(db.Model):
    __tablename__ = 'resume'

    id_resume = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)
    about_me = db.Column(db.Text)

    works = db.relationship('Work', backref='related_resume', lazy=True)
    educations = db.relationship('Education', backref='resume')
    projects = db.relationship('Projects', backref='resume')
