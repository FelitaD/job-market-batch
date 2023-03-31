from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.database import Postgresql
from diagrams.onprem.workflow import Airflow
from diagrams.programming.language import Python
from diagrams.onprem.analytics import Tableau
from diagrams.custom import Custom
from diagrams.generic.blank import Blank


with Diagram(name='Data lifecycle', outformat="jpg", show=False):

    with Cluster('Data sources'):
        web = Custom('Web', 'web.png')

    with Cluster('Pipelines'):
        with Cluster('Storage'):
            db = Postgresql('SQL database')
            b1 = Blank('')
            b2 = Blank('')
            e = Edge(color='#E0F4FC')
            b1 - e - db - e - b2

        with Cluster('Ingestion'):
            crawler = Python('Crawler')

        with Cluster('Transformation'):
            etl = Python('ETL pipeline')

        with Cluster('Serving'):
            api = Python('REST API')

    with Cluster('Analytics'):
        viz = Tableau('Tableau')

    airflow = Airflow('Orchestration')
    b3 = Blank('')
    b4 = Blank('')
    b5 = Blank('')
    e2 = Edge(color='white')
    b3 - e2 - b4 - e2 - airflow - e2 - b5

    web >> crawler >> etl >> api >> viz
