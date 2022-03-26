import os
import pandas as pd
import spacy

from config.definitions import PROJECT_PATH, TECHNOS


class TechnosAdder:
    """Extract in new column technologies cited in job's text based on the NER model or a custom list."""

    def __init__(self, jobs, language='en'):
        self.jobs = jobs
        self.language = language
        self.model_path = os.path.join(PROJECT_PATH, f'etl/transform/data/model_{language}/model-best')

    def add_technos_from_model(self):
        self.jobs['technos'] = self.jobs['text'].apply(lambda x: self.extract_ner_technos(x))

    def add_technos_from_custom_list(self):
        self.jobs['technos'] = self.jobs['text'].apply(lambda x: self.extract_custom_technos(x))

    def extract_ner_technos(self, text):
        model_output = spacy.load(self.model_path)
        doc = model_output(text)
        technos = [ent.text for ent in doc.ents]
        return list(set(technos))

    def extract_custom_technos(self, text):
        technos = [w for w in text.split(' ') if w in TECHNOS]
        return list(set(technos))
