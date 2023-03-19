from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.database import Postgresql
from diagrams.onprem.workflow import Airflow
from diagrams.programming.language import Python
from diagrams.onprem.analytics import Tableau
from diagrams.generic.database import SQL
from diagrams.custom import Custom
from diagrams.generic.blank import Blank


with Diagram(name='Data lifecycle', outformat="jpg", show=False):

    with Cluster('Storage'):
        raw = Postgresql('Raw data')
        processed = Postgresql('Transformed data')
        b1 = Blank('')
        b2 = Blank('')
        e = Edge(color='#E0F4FC')
        b1 - e - raw - e - processed - e - b2

    with Cluster('Data sources'):
        web = Custom('Web', 'web.png')

    with Cluster('Ingestion'):
        crawler = Python('Crawler')

    with Cluster('Transformation'):
        etl = Python('ETL pipeline')

    with Cluster('Serving'):
        viz = Tableau('Analytics')

    web >> crawler >> etl >> viz
