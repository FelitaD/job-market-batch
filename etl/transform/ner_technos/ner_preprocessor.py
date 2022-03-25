import re
import os
import pandas as pd
import spacy
from spacy import displacy
from spacy.tokens import DocBin
from tqdm import tqdm

from config.definitions import PROJECT_PATH

class NERPreprocessor:
    """Prepare training data for Name Entity Recognition model of technologies in jobs' text."""

    def __init__(self, jobs, language = 'en'):
        self.language = language
        self.jobs = jobs
        self.technos = {'(No)SQL', 'AWS', 'AWS Glue', 'AWS Redshift', 'AWS S3', 'Airbyte', 'Airflow', 'Akka',
                        'Apache Airflow', 'Apache Beam', 'Apache Kafka', 'Apollo', 'Astronomer', 'Athena', 'Azure',
                        'Bash', 'Beam', 'BigQuery', 'Bigtable', 'C#', 'C/C\\+\\+', 'Cassandra', 'Celery', 'Ceph',
                        'CircleCI', 'ClickHouse', 'CloudSQL', 'CockroachDB', 'Codecov', 'DAX', 'DataBuildTool',
                        'DataStudio', 'Datadog', 'Dataflow', 'Django', 'Docker', 'DynamoDB', 'EC2', 'EMR', 'ETL',
                        'ElasticSearch', 'Elasticsearch', 'Fivetran', 'Flink', 'Flyte', 'GCP', 'Git', 'Github',
                        'Gitlab', 'Glue', 'Go', 'Go lang', 'Golang', 'Google Cloud', 'Google Cloud Platform', 'Grafana',
                        'GraphQL', 'H20', 'HBase', 'HDFS', 'HTTP', 'Hadoop', 'Hive', 'IAM', 'Informatica', 'Istio',
                        'Java', 'Javascript', 'Jenkins', 'K8S', 'Kafka', 'Kibana', 'Kimball', 'Kinesis', 'Kubeflow',
                        'Kubernetes', 'LAMP', 'Linux', 'Looker', 'Luigi', 'MAPR', 'MS-SQL', 'MapReduce', 'Matillion',
                        'Matillion WTL', 'Metabase', 'Microsoft Azure', 'Microsoft SSIS', 'Microstrategy', 'Mongo',
                        'MongoDB', 'MxNet', 'MySQL', 'Neo4J', 'NiFi', 'NoSQL', 'Node', 'Numpy', 'OpenTSDB', 'Oracle',
                        'PHP', 'PQL', 'Pagerduty', 'Pandas', 'Perl', 'Pig', 'PostgreSQL', 'Postgres', 'PowerBI',
                        'Prometheus', 'Protobuf', 'Pub/Sub', 'PubSub', 'Py torch', 'PyTorch', 'Python', 'Qlikview',
                        'Quicksilver', 'R', 'RabbitMQ', 'React', 'Reddis', 'Redis', 'Redshift', 'Redshift Spectrum',
                        'Ruby', 'S3', 'SAP', 'SPAR', 'SQL', 'SQL Server', 'SQL server', 'SageMaker', 'Salt', 'Scala',
                        'Scikit Learn', 'Scipy', 'Shell', 'Snowflake', 'Spanner', 'Spark', 'SparkSQL', 'Stackdriver',
                        'StitchData', 'Synapse', 'Tableau', 'Talend', 'TensorFlow', 'Tensorflow', 'Typescript', 'UNIX',
                        'Unix', 'Unix Shell', 'Vitess', 'VizQL', 'airflow', 'data vault', 'dataiku', 'dbt', 'gRPC',
                        'git', 'k8s', 'mlflow', 'nodejs', 'python', 's3'}
        self.train_data_path = os.path.join(PROJECT_PATH, 'etl/transform/data/train_data')

    def prepare_training(self):
        jobs = self.jobs[self.jobs['language'] == self.language]
        collective_dict = {'TRAINING_DATA': []}

        for i in range(100):
            results = self.structure_training_data(jobs.loc[i, 'text'], self.technos)
            collective_dict['TRAINING_DATA'].append(results)

        train_data = collective_dict['TRAINING_DATA'][:50]
        train_data_doc = self.create_training(train_data, self.language)
        train_data_doc.to_disk(os.path.join(self.train_data_path, 'train_data.spacy'))

        valid_data = collective_dict['TRAINING_DATA'][50:]
        valid_data_doc = self.create_training(valid_data, self.language)
        valid_data_doc.to_disk(os.path.join(self.train_data_path, 'valid_data.spacy'))

    @staticmethod
    def structure_training_data(text, kw_list):
        entities = []

        for kw in tqdm(kw_list):
            search_ = re.finditer(kw, text, flags=re.IGNORECASE)
            matches_positions = [[m.start(), m.end()] for m in search_]

            if len(matches_positions) > 0:
                for match_positions in matches_positions:
                    start = match_positions[0]
                    end = match_positions[1]
                    entities.append((start, end, "TECHNO"))
            else:
                print("No pattern matches found. Keyword: ", kw)

        if len(entities) > 0:
            results = [text, {'entities': entities}]
            return results

    @staticmethod
    def create_training(train_data, language):
        nlp = spacy.blank(language)
        db = DocBin()

        for text, annot in tqdm(train_data):
            doc = nlp.make_doc(text)
            ents = []

            for start, end, label in annot['entities']:
                span = doc.char_span(start, end, label=label, alignment_mode='contract')
                if span is None:
                    print('Skipping entity.')
                else:
                    ents.append(span)
                    try:
                        doc.ents = ents
                    except:
                        ents.pop()
            doc.ents = ents
            db.add(doc)
        return db
