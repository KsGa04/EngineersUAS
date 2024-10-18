from Client_Api.extensions import db


class Responsibility(db.Model):
    __tablename__ = 'responsibilities'

    id_responsibility = db.Column(db.Integer, primary_key=True)
    id_work = db.Column(db.Integer, db.ForeignKey('work.id_work'), nullable=False)
    responsibility = db.Column(db.Text)
