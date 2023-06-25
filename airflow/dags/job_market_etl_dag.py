from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

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

    wttj_links_spider = BashOperator(
        task_id='wttj_links_spider',
        bash_command='python3 /Users/donor/Library/Mobile\ Documents/com~apple~CloudDocs/PycharmProjects/data-job-crawler/data_job_crawler/crawler/spiders'
                     '/wttj_links.py',
    )

    wttj_spider = BashOperator(
        task_id='wttj_spider',
        bash_command='python3 /Users/donor/Library/Mobile\ Documents/com~apple~CloudDocs/PycharmProjects/data-job-crawler/data_job_crawler/crawler/spiders/wttj.py',
        do_xcom_push=False
    )

    upload_new_links = BashOperator(
        task_id='upload_new_links',
        bash_command='python3 /Users/donor/Library/Mobile\ Documents/com~apple~CloudDocs/PycharmProjects/data-job-crawler/data_job_crawler/helpers/s3_helper.py'
    )

    from data_job_etl.etl import main
    etl = PythonOperator(
        task_id='etl',
        python_callable=main,
    )

    message = BashOperator(
        task_id='message',
        bash_command='python3 /Users/donor/Library/Mobile\ Documents/com~apple~CloudDocs/PycharmProjects/data-job-etl/data_job_etl/message.py'
    )


wttj_links_spider >> upload_new_links >> wttj_spider >> create_tables >> etl >> message
