from Client_Api.extensions import db


class Group(db.Model):
    __tablename__ = 'groups_number'

    id_group = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50))
    start_year = db.Column(db.Integer)
    id_university = db.Column(db.Integer, db.ForeignKey('university.id_university'), nullable=False)
    id_direction = db.Column(db.Integer, db.ForeignKey('direction.id_direction'), nullable=False)
