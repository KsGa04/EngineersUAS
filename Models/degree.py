from Client_Api.extensions import db


class Degree(db.Model):
    __tablename__ = 'degree'

    id_degree = db.Column(db.Integer, primary_key=True)
    degree_name = db.Column(db.String(255), nullable=False)
