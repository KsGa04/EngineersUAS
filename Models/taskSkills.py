from Client_Api.extensions import db


class TaskSkill(db.Model):
    __tablename__ = 'task_skills'

    id = db.Column(db.Integer, primary_key=True)
    id_task = db.Column(db.Integer, db.ForeignKey('tasks.id_task'), nullable=False)
    id_skill = db.Column(db.Integer, db.ForeignKey('skills.id_skill'), nullable=False)
