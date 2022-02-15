from db import db


class JobModel(db.Model):
    """
    Internal representation of the Job resource and helper.
    Client doesn't interact directly with these methods.
    """
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(80), db.ForeignKey('companies.name'))
    company_rel = db.relationship('CompanyModel')
    remote = db.Column(db.Integer)

    def __init__(self, id, company, remote):
        self.id = id
        self.company = company
        self.remote = remote

    def json(self):
        return {'id': self.id, 'company': self.company, 'remote': self.remote}

    @classmethod
    def find_by_id(cls, id):
        return JobModel.query.filter_by(id=id).first()  # returns JobModel instance with init attributes

    def save_to_db(self):
        """ Upsert : update or insert """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
