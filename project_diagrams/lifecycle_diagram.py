from diagrams import Diagram, Cluster
from diagrams.onprem.database import Postgresql
from diagrams.onprem.workflow import Airflow
from diagrams.programming.language import Python
from diagrams.onprem.analytics import Tableau
from diagrams.generic.database import SQL
from diagrams.custom import Custom


with Diagram(outformat="jpg", show=False):
    web_wttj = Custom('wttj.com/jobs', './welcome-to-the-jungle-squarelogo-1602063832341.png')
    web_spotify = Custom('lifeatspotify.com/jobs', './Spotify_icon.png')
    raw_db = Postgresql('Raw data')
    processed_db = Postgresql('Processed data')
    pivotted_db = Postgresql('Pivotted data')

    with Cluster('Data sources'):

    with Cluster('Ingestion'):

    with Cluster('Transformation'):
        preprocessor = Python('Preprocessor')
        technos_processor = Python('TechnosProcessor')
        loader = Python('Loader')

    with Cluster('Serving'):
        viz = Tableau('Tableau')
        olap = SQL('OLAP queries')

    web_wttj >> wttj_links
    web_spotify >> spotify_links

    wttj_links >> wttj
    spotify_links >> spotify
    [wttj, spotify] >> scrapy_pipeline >> raw_db

    raw_db >> preprocessor >> technos_processor >> loader >> [processed_db, pivotted_db]

    pivotted_db >> viz
    processed_db >> olap
