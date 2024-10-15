from Client_Api.extensions import db


class Resume(db.Model):
    __tablename__ = 'resume'
    id_resume = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user', ondelete='CASCADE'))
    resume_title = db.Column(db.String(255))
    short_description = db.Column(db.Text)
    about_me = db.Column(db.Text)

    user_rel = db.relationship('User', backref='resumes')