# Data (engineering) Job Market

A batch pipeline to analyse job postings.<br>
The project uses Airflow to orchestrate the batch pipeline consisting of a Scrapy crawler, a Postgres database and Python scripts to perform ETL.

- [Prerequesites](##Prerequesites)
  - [Install Airflow](###Install Airflow)
  - [Run Airflow in standalone (development)](###Run Airflow in standalone (development))
  - [Create Postgres database](###Create Postgres database)
  - [Install custom packages](###Install custom packages)
- [Run the project](##Run the project)
- [Tests](##Tests)
  - [Manual tests](###Manual tests)
  - [DAG import error tests](###DAG import error tests)
- [Roadmap](##Roadmap)

## Prerequesites
### Install Airflow

From [Airflow doc](https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html) installation instructions :

- Change airflow home in bash/zsh profile

```export AIRFLOW_HOME=[...]/job-market-batch/airflow```

- Install Airflow using the constraints file

```
AIRFLOW_VERSION=2.3.3
PYTHON_VERSION="$(python3 --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip3 install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

### Run Airflow in standalone (development)
Standalone mode : initialise the Airflow database, make a user, and start all components.

```airflow standalone```
Visit `localhost:8080` in the browser and use the admin account details shown on the terminal to login.

### Create Postgres database

Will contain the job postings.
- Install Postgres
- Create database
- Add username `JOB_MARKET_DB_USER` and password `JOB_MARKET_DB_PWD` environment variables 

### Install custom packages

> Airflow's best practice to import custom code is through packages.

Install packages corresponding to 2 phases of the pipeline :
- Data ingestion : [data-job-crawler](https://pypi.org/project/data-job-crawler/)
- Data processing : [data-job-etl](https://pypi.org/project/data-job-etl/)

- Execute `playwright install` to enable playwright library used to scrape Javascript web pages.

## Run the project

- Airflow UI :<br>
Connect on localhost:8080 with username `admin` and password in `standalone_admin_password.txt`.<br> 
In the DAGs tab, toggle on job-market-batch. Trigger the DAG manually if it's not running.
- Postgres tables :<br> `raw_jobs` contains data before transform<br> `pivotted_jobs` contains the processed data with 1 skill per job and per row for usage in Tableau.

## Tests

### Manual tests

1. As soon as the DAG finished, we can look at the logs in Airflow UI for tracebacks.
2. Check modification date of `wttj_links.txt` and `spotify_links.txt`.
3. Look into Postgres `raw_jobs` and query most recent data.
4. Compare with `pivotted_jobs` table.

### DAG import error tests

The loading time of DAG is one that has biggest impact on scheduler's performance.

Running this command : `time python3 airflow/dags/job_market_etl_dag.py`
returns : `python3 airflow/dags/job_market_etl_dag.py  65.12s user 5.28s system 53% cpu 2:11.90 total`

The first measure is the real time, so how long the DAG took to process, here 65.12 seconds, hence generating a DAG import error because it exceeds the 30 s recommended.

> Changing Import Timeout
> 
> `export AIRFLOW__CORE__DAGBAG_IMPORT_TIMEOUT=300`<br>
> `airflow config list|grep -i timeout`

#### Test individual task

`airflow tasks test dag_id task_id date`

## Roadmap

- [ ] Add unit tests https://airflow.apache.org/docs/apache-airflow/2.3.3/best-practices.html#best-practices-dag-loader-test
- [ ] Add Airflow DAG documentation