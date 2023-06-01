from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.database import Postgresql
from diagrams.onprem.workflow import Airflow
from diagrams.programming.language import Python
from diagrams.onprem.analytics import Tableau
from diagrams.onprem.client import Client
from diagrams.custom import Custom
from diagrams.generic.blank import Blank
from diagrams.aws.storage import SimpleStorageServiceS3Bucket


with Diagram(name='Data lifecycle', outformat="jpg", show=True):
    with Cluster('Data sources'):
        web = Custom('Web', 'docs/web.png')

    with Cluster('Pipelines'):
        with Cluster('Storage'):
            db = Postgresql('PostgreSQL')
            s3 = SimpleStorageServiceS3Bucket('S3')
            b1 = Blank('')
            b2 = Blank('')
            e = Edge(color='#E0F4FC')
            s3 - e - db - e - b1

        with Cluster('Ingestion'):
            crawler = Python('Crawler')

        with Cluster('Transformation'):
            etl = Python('ETL pipeline')

        with Cluster('Serving'):
            api = Python('REST API')

    with Cluster('Usage'):
        viz = Tableau('Tableau')
        mail = Custom('Email', 'docs/email.png')
        jupyter = Custom('Jupyter', 'docs/jupyter.jpg')
        web_ui = Client('Web UI')

    airflow = Airflow('Orchestration')
    b3 = Blank('')
    b4 = Blank('')
    b5 = Blank('')
    e2 = Edge(color='white')
    b3 - e2 - b4 - e2 - airflow - e2 - b5

    web >> crawler >> etl >> api >> mail
