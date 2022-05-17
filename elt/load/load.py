import os
import pandas as pd
import ast
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import IntegrityError
import json

from config.definitions import DB_STRING, DATA_PATH
from config.postgres_schema import ProcessedJob, Base


def run_loader(**context):
    loader = Loader()
    loader.load()

    context['ti'].xcom_push(
        key='length_jobs',
        value=len(loader.jobs)
    )


class Loader:

    def __init__(self):
        self.jobs = pd.read_csv(os.path.join(DATA_PATH, 'processed_jobs_from_custom_list.csv'))

    def load(self):
        engine = create_engine(DB_STRING, echo=True)
        db_session = sessionmaker(bind=engine)

        Base.metadata.create_all(engine)
        Base.metadata.bind = engine

        for i in range(len(self.jobs)):
            url = self.jobs.loc[i, 'url']
            title = self.jobs.loc[i, 'title']
            company = self.jobs.loc[i, 'company']
            industry = self.jobs.loc[i, 'industry']
            stack = self.jobs.loc[i, 'technos']
            location = self.jobs.loc[i, 'location']
            remote = self.jobs.loc[i, 'remote']
            _type = self.jobs.loc[i, 'type']
            language = self.jobs.loc[i, 'language']
            created_at = self.jobs.loc[i, 'created_at']
            text = self.jobs.loc[i, 'text']

            job = ProcessedJob(url=url,
                               title=title,
                               company=company,
                               industry=industry,
                               stack=stack,
                               location=location,
                               remote=remote,
                               type=_type,
                               language=language,
                               created_at=created_at,
                               text=text)

            with engine.connect() as connection:
                with db_session(bind=connection) as session:
                    session.begin()
                    try:
                        session.merge(job)
                        session.commit()
                    except:
                        session.rollback()
