import pandas as pd
import os

from preprocess.preprocess import Preprocessor
from ner_technos.ner_preprocessor import NERPreprocessor
from ner_technos.train_model import NERTrainer
from config.definitions import PROJECT_PATH

data_path = os.path.join(PROJECT_PATH, 'etl/transform/data', 'preprocessed_jobs.csv')

preprocessor = Preprocessor()
preprocessor.preprocess()
preprocessor.jobs.to_csv(data_path)

jobs = pd.read_csv(data_path)
techno_recogniser = NERPreprocessor(jobs)
techno_recogniser.prepare_training()

ner_trainer = NERTrainer()
ner_trainer.init_config()
ner_trainer.train()


