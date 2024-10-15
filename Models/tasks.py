from Client_Api.extensions import db


class Tasks(db.Model):
    __tablename__ = 'tasks'
    id_task = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(255))
    task_type = db.Column(db.String(50))
    id_group = db.Column(db.Integer, db.ForeignKey('group.id_group'))
    task_description = db.Column(db.Text)