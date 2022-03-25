import os
import pandas as pd
import spacy

from config.definitions import PROJECT_PATH


class TechnosAdder:
    def __init__(self, jobs, language='en'):
        self.jobs = jobs
        self.language = language
        self.model_path = os.path.join(PROJECT_PATH, f'etl/transform/data/model_{language}/model-best')

    def add_technos(self):
        self.jobs['technos'] = self.jobs['text'].apply(lambda x: self.extract_technos(x))

    def extract_technos(self, text):
        model_output = spacy.load(self.model_path)
        doc = model_output(text)
        technos = [ent.text for ent in doc.ents]
        return list(set(technos))
