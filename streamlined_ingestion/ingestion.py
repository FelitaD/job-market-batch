import pandas as pd
from sqlalchemy import create_engine

from definitions import USER, PASSWORD

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)

db_string = f"postgresql://{USER}:{PASSWORD}@localhost:5432/job_market"
engine = create_engine(db_string)

jobs = pd.read_sql("jobs", engine)

print(jobs.head())