import os
import pandas as pd
import ast
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError


from config.definitions import DB_STRING_V2, DATA_PATH
from job_market_schema import Company, Job, Techno, Base


class Loader:

    def __init__(self):
        self.jobs = pd.read_csv(os.path.join(DATA_PATH, 'processed_jobs_from_custom_list.csv'))

    def load(self):
        engine = create_engine(DB_STRING_V2, echo=True)

        Base.metadata.create_all(engine)
        Base.metadata.bind = engine
        db_session = sessionmaker()
        db_session.bind = engine
        session = db_session()

        for i in range(len(self.jobs[:10])):
            title = self.jobs.loc[i, 'title']
            url = self.jobs.loc[i, 'url']
            _type = self.jobs.loc[i, 'type']
            location = self.jobs.loc[i, 'location']
            remote = self.jobs.loc[i, 'remote']
            language = self.jobs.loc[i, 'language']
            company_name = self.jobs.loc[i, 'company']
            text = self.jobs.loc[i, 'text']
            job = Job(company_name=company_name, title=title, url=url, type=_type, location=location, remote=remote, language=language, text=text)

            industry = self.jobs.loc[i, 'industry']
            company = Company(name=company_name, industry=industry)

            # company.jobs.append(job)
            try:
                session.merge(company)
                session.merge(job)
            except IntegrityError:
                session.rollback()

            technos = ast.literal_eval(self.jobs.loc[i, 'technos'])
            for j in range(len(technos)):
                techno_name = technos[j]
                category = ''
                techno = Techno(name=techno_name, category=category)
                try:
                    session.merge(techno)
                except IntegrityError:
                    session.rollback()

            session.commit()


        # inspector = inspect(engine)
        # print(inspector.get_table_names())


Loader().load()