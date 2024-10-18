from Client_Api.extensions import db


class WorkOrganization(db.Model):
    __tablename__ = 'work_organization'

    id = db.Column(db.Integer, primary_key=True)
    id_work = db.Column(db.Integer, db.ForeignKey('work.id_work'), nullable=False)
    id_organization = db.Column(db.Integer, db.ForeignKey('organization.id_organization'), nullable=False)

