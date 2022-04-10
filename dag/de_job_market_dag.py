from datetime import timedelta, datetime
from airflow import DAG
from airflow.utils.task_group import TaskGroup
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.models.connection import Connection
from airflow.sensors.filesystem import FileSensor

from elt.transform.transform import transform
from elt.load.load import run_loader
from elt.load.create_tables import create_tables

dag_id = 'DE_job_market'

default_args = {
    'start_date': datetime(2022, 4, 1)
}

with DAG(dag_id=dag_id, default_args=default_args, catchup=False, schedule_interval='@daily') as dag:
    create_tables = PythonOperator(
        task_id='create_tables',
        python_callable=create_tables
    )

    with TaskGroup('crawler') as crawler:
        with TaskGroup('links_spiders') as links_spiders:
            wttj_links_spider = BashOperator(
                task_id='wttj_links_spider',
                bash_command='python3 /Users/donor/PycharmProjects/DE_job_market/elt/extract/jobs_crawler/spiders/wttj_links.py'
            )

            spotify_links_spider = BashOperator(
                task_id='spotify_links',
                bash_command='python3 /Users/donor/PycharmProjects/DE_job_market/elt/extract/jobs_crawler/spiders/wttj_links.py',
                do_xcom_push=False
            )

        datai_spider = BashOperator(
            task_id='datai_spider',
            bash_command='python3 /Users/donor/PycharmProjects/DE_job_market/elt/extract/jobs_crawler/spiders/datai.py',
            do_xcom_push=False
        )

        wttj_spider = BashOperator(
            task_id='wttj_spider',
            bash_command='python3 /Users/donor/PycharmProjects/DE_job_market/elt/extract/jobs_crawler/spiders/wttj.py',
            do_xcom_push=False
        )

        spotify_spider = BashOperator(
            task_id='spotify_spider',
            bash_command='python3 /Users/donor/PycharmProjects/DE_job_market/elt/extract/jobs_crawler/spiders/wttj.py',
            do_xcom_push=False
        )

    transformer = PythonOperator(
        task_id='transformer',
        python_callable=transform,
        provide_context=True
    )

    loader = PythonOperator(
        task_id='loader',
        python_callable=run_loader,
        provide_context=True
    )

create_tables >> [wttj_links_spider, spotify_links_spider, datai_spider]

wttj_links_spider >> wttj_spider
spotify_links_spider >> spotify_spider

[wttj_spider, spotify_spider, datai_spider] >> transformer >> loader
