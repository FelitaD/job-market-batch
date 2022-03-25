import pandas as pd
import os

from config.definitions import PROJECT_PATH
from preprocess.preprocess import Preprocessor
from ner_technos.ner_preprocessor import NERPreprocessor
from ner_technos.train_model import NERTrainer
from ner_technos.add_technos import TechnosAdder

data_path = os.path.join(PROJECT_PATH, 'etl/transform/data')

# preprocessor = Preprocessor()
# preprocessor.preprocess()
#
# preprocessor.jobs.to_csv(data_path)
jobs = pd.read_csv(os.path.join(data_path, 'preprocessed_jobs.csv'))

# techno_recogniser = NERPreprocessor(jobs)
# techno_recogniser.prepare_training()
#
# ner_trainer = NERTrainer()
# ner_trainer.init_config()
# ner_trainer.train()

techno_adder = TechnosAdder(jobs)
techno_adder.add_technos()
techno_adder.jobs.to_csv(os.path.join(data_path, 'processed_jobs.csv'))



