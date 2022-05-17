import os
import pandas as pd
# import spacy
import json

from config.definitions import PROJECT_PATH, TECHNOS


class TechnosProcessor:
    """Extract in new column technologies cited in job's text based on the NER model or a custom list."""

    def __init__(self, jobs, language='en'):
        self.jobs = jobs
        self.language = language
        self.model_path = os.path.join(PROJECT_PATH, f'elt/transform/data/model_{language}/model-best')

    def process_technos(self):
        technos_expanded = self.add_technos_from_custom_list()
        technos_pivotted = self.pivot_technos(technos_expanded)
        df_cleaned = self.clean_df(technos_pivotted)
        print(df_cleaned.columns)
        technos_mapped = self.map_techno_lower_to_pretty(df_cleaned)
        print(technos_mapped.columns)
        return technos_mapped

    def add_technos_from_custom_list(self):
        """Add a 'stack' column containing a list of technologies present in the text of the job posting
        then expand this list in as many columns as there are elements in the list."""
        self.jobs['stack'] = self.jobs['text'].apply(lambda x: self.extract_custom_technos(x))
        technos = pd.DataFrame(self.jobs['stack'].to_list())
        df = pd.merge(self.jobs, technos, left_index=True, right_index=True)
        return df

    @staticmethod
    def pivot_technos(df):
        unpivotted_columns = ['url', 'title', 'company', 'location', 'type', 'industry', 'remote', 'created_at',
                              'text', 'language', 'stack']
        pivotted_technos = pd.melt(df, id_vars=unpivotted_columns).sort_values(by=['company', 'created_at', 'title'])
        pivotted_technos.reset_index(drop=True, inplace=True)
        return pivotted_technos

    @staticmethod
    def clean_df(df):
        df['technos'] = df['value']
        df.drop(['variable', 'stack', 'value'], axis=1, inplace=True)
        df.dropna(subset='technos', inplace=True)
        return df

    @staticmethod
    def map_techno_lower_to_pretty(df):
        mapper = pd.read_csv('/Users/donor/PycharmProjects/DE_job_market/elt/transform/data/technos_lower_to_pretty.csv', sep=';')
        lower = mapper.Skills_lower.values
        pretty = mapper.Skills_pretty.values
        mapper_dict = dict(zip(lower, pretty))
        df['technos'] = df['technos'].map(mapper_dict)
        return df

    @staticmethod
    def extract_custom_technos(text):
        technos = [w.lower() for w in text.split(' ') if w.lower() in TECHNOS]
        return list(set(technos))

    # def add_technos_from_model(self):
    #     self.jobs['technos'] = self.jobs['text'].apply(lambda x: self.extract_ner_technos(x))

    # def extract_ner_technos(self, text):
    #     model_output = spacy.load(self.model_path)
    #     doc = model_output(text)
    #     technos = [ent.text for ent in doc.ents]
    #     return list(set(technos))
