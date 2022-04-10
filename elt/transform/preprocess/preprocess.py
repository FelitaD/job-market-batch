import pandas as pd
import numpy as np
import re
from sqlalchemy import create_engine
from langdetect import detect

from config.definitions import DB_STRING


class Preprocessor:

    def __init__(self):
        self.engine = create_engine(DB_STRING)
        self.jobs = pd.read_sql('jobs', self.engine)

    def preprocess(self, **context):
        self.jobs.drop('id', axis=1, inplace=True)
        self.jobs = self.jobs.convert_dtypes()
        self.jobs['created_at'] = pd.to_datetime(self.jobs['created_at'])
        self.jobs['remote'].replace('N', np.nan, inplace=True)
        self.jobs['title'] = self.jobs['title'].apply(lambda x: self.preprocess_title(x))
        self.jobs = self.detect_and_delete_language(self.jobs)
        self.jobs['text'] = self.jobs['text'].apply(lambda x: self.preprocess_text(x))
        self.jobs.reset_index(inplace=True)

    @staticmethod
    def preprocess_title(title):
        # (H/F), H/F, H / F, (F/H), F/H, (M/F), M/F, (F/M), F/M, M/W, (HF),(M/F/D), (F/H/X), (m/f/d), (m/w/d), (H/S/T)
        gender_regex = '[\(]?[HFMWDXmfdwST]{1}[\s]?[\/]{1}[\s]?[HFMWDXmfdwST]{1}[\)]?[\/]?[HFMWDXmfdwST]?[\)]?'
        title = re.sub(gender_regex, '', title)
        # Empty parenthesis
        title = re.sub('\([\s]?\)', '', title)
        # Special characters
        title = re.sub('[|#]', '', title)
        title = title.strip()
        return title

    @staticmethod
    def detect_and_delete_language(jobs):
        jobs['language'] = jobs['text'].apply(lambda x: detect(x))
        jobs.drop(jobs[(jobs['language'] != 'en') & (jobs['language'] != 'fr')].index, axis=0, inplace=True)
        return jobs

    @staticmethod
    def preprocess_text(text):
        # Remove newline at beginning of text
        text = re.sub('^[\\]n[\s]*', '', text)
        # Remove \xa0 (non-breaking space in Latin1 ISO 8859-1)
        text = text.replace(u'\xa0', u' ')
        # Replace newlines if there is more than 3
        text = re.sub('[\s]{3,10}', '\n\n', text)
        return text
