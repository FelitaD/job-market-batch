from datetime import timedelta, datetime
from airflow import DAG
from airflow.utils.task_group import TaskGroup
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.models.connection import Connection
from airflow.sensors.filesystem import FileSensor

dag_id = 'job-market-batch'

default_args = {
    'start_date': datetime(2022, 4, 1)
}

with DAG(dag_id=dag_id,
         default_args=default_args,
         max_active_runs=1,
         max_active_tasks=1,
         catchup=False,
         schedule_interval='@daily') as dag:

    from data_job_etl.load.create_tables import create_tables
    create_tables = PythonOperator(
        task_id='create_tables',
        python_callable=create_tables
    )

    with TaskGroup('crawler') as crawler:

        wttj_links_spider = BashOperator(
            task_id='wttj_links_spider',
            bash_command='python3 /Users/donor/PycharmProjects/data-job-crawler/data_job_crawler/crawler/spiders/wttj_links.py',
        )

        wttj_spider = BashOperator(
            task_id='wttj_spider',
            bash_command='python3 /Users/donor/PycharmProjects/data-job-crawler/data_job_crawler/crawler/spiders/wttj.py',
            do_xcom_push=False
        )

        spotify_links_spider = BashOperator(
            task_id='spotify_links_spider',
            bash_command='python3 /Users/donor/PycharmProjects/data-job-crawler/data_job_crawler/crawler/spiders/spotify_links.py',
        )

        spotify_spider = BashOperator(
            task_id='spotify_spider',
            bash_command='python3 /Users/donor/PycharmProjects/data-job-crawler/data_job_crawler/crawler/spiders/spotify.py',
            do_xcom_push=False
        )

    from data_job_etl.etl import transform_and_load
    etl = PythonOperator(
        task_id='etl',
        python_callable=transform_and_load,
    )

create_tables >> [spotify_links_spider, wttj_links_spider]

wttj_links_spider >> wttj_spider
spotify_links_spider >> spotify_spider

crawler >> etl
