from db import db


class CompanyModel(db.Model):
    """
    Internal representation of the Job resource and helper.
    Client doesn't interact directly with these methods.
    """
    __tablename__ = 'companies'

    name = db.Column(db.String(80), primary_key=True)

    jobs = db.relationship('JobModel', lazy='dynamic') # won't call table unless use json method

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'jobs': [job.json() for job in self.jobs.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # returns JobModel instance with init attributes

    def save_to_db(self):
        """ Upsert : update or insert """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
