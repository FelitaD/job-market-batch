# Data Engineering Job Market

The purpose of this project is to have a better idea of the data engineering job market. 
The goal is to answer certain questions for my job hunt in order to skill up in the right areas. For example, what technologies are the most used by companies in Europe ? What data stack is the most asked for Junior positions ? Etc.

Doc :
- Pipeline Architecture
- Database Schema
  - Functional dependencies and decomposition in BCNF
  - Multivalued dependencies and decomposition in 4NF
- How to run the project
- How to test the project

## Pipeline Architecture

The project runs locally with Airflow to orchestrate a batch pipeline consisting of a crawler, an ETL process and an API to query a Postgres database.

**Remarks** <br>
- The crawler and the ETL scripts are encapsulated in packages to follow Airflow's best practice[^1](https://airflow.apache.org/docs/apache-airflow/2.2.0/modules_management.html) to add custom code. Their repositories contain more detailed documentation for each process :
  - [data-job-crawler](https://github.com/FelitaD/data-job-crawler)
  - [data-job-etl](https://github.com/FelitaD/data-job-etl)
- The choice of an ETL process is more appropriate than an ELT due to the relational data, relatively small and requiring complex transformations.

**Diagrams**

Diagrams are generated through [Structurizr's API](https://structurizr.com/workspace/79499/diagrams) with the command
```bash
structurizr-cli -id WORKSPACE_ID -key STRUCTURIZR_KEY -secret STRUCTURIZR_SECRET -workspace WORKSPACE_FILE
```
`WORKSPACE_ID = 79499`<br>
The C4 model is used because it is text-based / version control and the project evolves a lot. 

## Database schema

The extracted data goes primarily into a schema with a single 'mega' relation : `mega.jobs`.

### Functional dependencies and decomposition in BCNF
Functional dependencies in `mega.jobs`:
- job_id -> url, title, company, location, type, remote, created_at, text
- company -> industry


## How to run the project

Everything in development stage (local).

- Install custom packages from pypi
  - Data ingestion : [data-job-crawler](https://pypi.org/project/data-job-crawler/)
  - Data processing : [data-job-etl](https://pypi.org/project/data-job-etl/)
- Execute `playwright install` to enable playwright library used to scrape Javascript web pages.

- Install Airflow : [installation instructions](https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html)
 
- Create Postgres database `job_market` with username `JOB_MARKET_DB_USER` and password `JOB_MARKET_DB_PWD` as environment variables. 

- Run ```airflow standalone``` to initialise the Airflow database, make a user, and start all components (development phase).<br>
- Visit Airflow UI `localhost:8080` in the browser and use the admin account details shown on the terminal to login, or
  - username `admin` 
  - password in `standalone_admin_password.txt` ou `findajob`
  - In the DAGs tab, toggle on job-market-batch. Trigger the DAG manually if it's not running.

## How to test the project

**Manual tests**

1. As soon as the DAG finished, we can look at the logs in Airflow UI for tracebacks.
2. Check modification date of `wttj_links.txt` and `spotify_links.txt`.
3. Look into Postgres `raw_jobs` and query most recent data.
4. Compare with `pivotted_jobs` table.

**DAG import error tests**

The loading time of DAG is one that has the biggest impact on scheduler's performance.

Running this command : `time python3 airflow/dags/job_market_etl_dag.py`
returns : `python3 airflow/dags/job_market_etl_dag.py  65.12s user 5.28s system 53% cpu 2:11.90 total`

The first measure is the real time, so how long the DAG took to process, here 65.12 seconds, hence generating a DAG import error because it exceeds the 30 s recommended.

> Changing Import Timeout
> 
> `export AIRFLOW__CORE__DAGBAG_IMPORT_TIMEOUT=300`<br>
> `airflow config list|grep -i timeout`

**Test individual task**

`airflow tasks test dag_id task_id date`

## Roadmap

- [ ] Add unit tests https://airflow.apache.org/docs/apache-airflow/2.3.3/best-practices.html#best-practices-dag-loader-test
- [ ] Add data-job-api
- [ ] Add visualisations