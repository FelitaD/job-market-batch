import pandas as pd
import os

from config.definitions import PROJECT_PATH, DATA_PATH
from preprocess.preprocess import Preprocessor
from ner_technos.ner_preprocessor import NERPreprocessor
from ner_technos.train_model import NERTrainer
from ner_technos.add_technos import TechnosAdder


# preprocessor = Preprocessor()
# preprocessor.preprocess()
#
# preprocessor.jobs.to_csv(DATA_PATH)
jobs = pd.read_csv(os.path.join(DATA_PATH, 'preprocessed_jobs.csv'))

# techno_recogniser = NERPreprocessor(jobs)
# techno_recogniser.prepare_training()
#
# ner_trainer = NERTrainer()
# ner_trainer.init_config()
# ner_trainer.train()

techno_adder = TechnosAdder(jobs)
techno_adder.add_technos_from_custom_list()
techno_adder.jobs.to_csv(os.path.join(DATA_PATH, 'processed_jobs_from_custom_list.csv'))



