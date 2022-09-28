# Data (engineering) Job Market

A batch pipeline to analyse job postings.<br>
The project uses Airflow to orchestrate the batch pipeline consisting of a Scrapy crawler, a Postgres database and Python scripts to perform ETL.

## Installations
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

### Run Airflow
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

One package has been created for 2 elements of the pipeline :
- [data-job-crawler](https://pypi.org/project/data-job-crawler/)
- [data-job-etl](https://pypi.org/project/data-job-etl/)

## Run the project

- Airflow UI :<br>
Connect on localhost:8080 with username `admin` and password in `standalone_admin_password.txt`.<br> 
In the DAGs tab, toggle on job-market-batch. Trigger the DAG manually if it's not running.
- Postgres tables :<br> `raw_jobs` contains data before transform<br> `pivotted_jobs` contains the processed data with 1 skill per job and per row for usage in Tableau.

### Manual tests

1. As soon as the DAG finished, we can look at the logs in Airflow UI for tracebacks.
2. Check modification date of `wttj_links.txt` and `spotify_links.txt`.
3. Look into Postgres `raw_jobs` and query most recent data.
4. Compare with `pivotted_jobs` table.