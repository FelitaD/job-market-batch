from numpy.random._generator import Sequence
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, inspect, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd

Base = declarative_base()


jobs_technos = Table('jobs_technos', Base.metadata,
    Column('job_id', ForeignKey('jobs.id'), primary_key=True),
    Column('techno_id', ForeignKey('technos.id'), primary_key=True)
)


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    industry = Column(String(100))

    jobs = relationship('Job', backref='companies')


class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'))
    url = Column(String(400), nullable=False, unique=True)
    type = Column(String(20))
    # location = Column(String(100))
    # remote = Column(String(100))
    # language = Column(String(2))
    # text = Column(String)

    technos = relationship('Techno', secondary=jobs_technos, backref='jobs')


class Techno(Base):
    __tablename__ = 'technos'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    category = Column(String(100))

    jobs = relationship('Job', secondary=jobs_technos, back_populates='technos')

