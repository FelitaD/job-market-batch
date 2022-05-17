from datetime import timedelta, datetime
from airflow import DAG
from airflow.utils.task_group import TaskGroup
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.models.connection import Connection
from airflow.sensors.filesystem import FileSensor


dag_id = 'DE_job_market'

default_args = {
    'start_date': datetime(2022, 4, 1)
}

with DAG(dag_id=dag_id,
         default_args=default_args,
         max_active_runs=1,
         max_active_tasks=1,
         catchup=False,
         schedule_interval='@daily') as dag:

    from elt.load.create_tables import create_tables
    create_tables = PythonOperator(
        task_id='create_tables',
        python_callable=create_tables
    )

    with TaskGroup('crawler') as crawler:

        wttj_links_spider = BashOperator(
            task_id='wttj_links_spider',
            bash_command='python3 /Users/donor/PycharmProjects/DE_job_market/elt/extract/jobs_crawler/spiders'
                         '/wttj_links.py',
        )

        spotify_links_spider = BashOperator(
            task_id='spotify_links',
            bash_command='python3 /Users/donor/PycharmProjects/DE_job_market/elt/extract/jobs_crawler/spiders'
                         '/spotify_links.py',
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

    from elt.transform.transform import transform
    transformer = PythonOperator(
        task_id='transformer',
        python_callable=transform,
    )

    from elt.load.load import run_loader
    loader = PythonOperator(
        task_id='loader',
        python_callable=run_loader,
    )

create_tables >> [spotify_links_spider, wttj_links_spider, datai_spider]

wttj_links_spider >> wttj_spider
spotify_links_spider >> spotify_spider

crawler >> transformer >> loader
