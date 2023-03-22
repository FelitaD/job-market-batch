# Data Engineering Job Market

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Testing](#testing)
  - [End-to-end tests](#end-to-end-tests)
  - [Data quality testing](#data-quality-testing)
  - [Monitoring](#monitoring)
  - [Unit testing](#unit-testing)
- [Data Lifecycle](#data-lifecycle)
  - [Source System](#source-system)
  - [Ingestion](#ingestion)
  - [Transformation](#transformation)
  - [Serving](#serving)
  - [Storage](#storage)
  - [Orchestration](#orchestration)
- [How to run](#how-to-run)

## Project Overview

The project's purpose is to obtain a better insight into the data engineering job market. 
The initial goal was to answer certain questions for my job hunt in order to skill up in the right areas. What technologies are the most used by companies in Europe? What data stack is the most asked for Junior positions? Etc.

This repo contains Airflow's DAG which uses custom code through python packages: 
- Crawler: [data-job-crawler](https://github.com/FelitaD/data-job-crawler)
- ETL pipeline: [data-job-etl](https://github.com/FelitaD/data-job-etl)  
- API: [data-job-api]()


## Architecture

![img](project_diagrams/data_lifecycle.jpg)

C4 model diagrams: https://structurizr.com/workspace/79499/diagrams

## Testing

Tests below do not measure intermediary steps. For individual pipelines tests see their respective repositories.

### Airflow Tests

- Test the DAG: `python3 job_market_etl_dag.py`
- Import time: `time python3 job_market_etl_dag.py`. Maximum is 30 seconds.
- Unit tests for loading the DAG: `pytest test/`
- Test tasks individually: 
  - `airflow tasks test job-market-batch create_tables 2022-01-01`
  - `airflow tasks test job-market-batch spotify_links_spider 2022-01-01`
  - `airflow tasks test job-market-batch wttj_links_spider 2022-01-01`
  - `airflow tasks test job-market-batch spotify_spider 2022-01-01`
  - `airflow tasks test job-market-batch wttj_spider 2022-01-01`
  - `airflow tasks test job-market-batch transform_and_load 2022-01-01`
- Backfill (takes account of dependencies): `airflow dags backfill job-market-batch --start-date 2023-01-01`

### End-to-end Test

Sometimes Airflow's tests will pass but not the DAG run because of the configuration file. For example, the `hostname_callable = socket:getfqdn` will return different hostname values from time to time, explaining the strange behaviour below (solution: set to `socket:gethostname`).

![dag_anomaly](project_diagrams/dag_anomaly.png)

After at least one successful DAG run (all tasks green and supposedly no errors in the logs), we can take a random website and query the final database with the same url.

Example:
```
SELECT title, company, technos, created_at, url FROM pivotted_jobs WHERE url LIKE 'https://www.welcometothejungle.com/fr/companies/foxintelligence/jobs/senior-data-analyst-team-quality_paris%' ORDER BY created_at;
```
TODO
- [ ] All technologies must be present
- [ ] Eliminate duplicates by changing the url field and removing the last part

### Data Quality Testing

[data quality testing](https://www.montecarlodata.com/blog-data-quality-testing/)

### Monitoring

To be completed.

### Unit Testing

To be completed.

## Data Lifecycle

### Source system

The data sources are the web pages containing results for the latest data engineering jobs.  The project started with [Spotify](https://www.lifeatspotify.com/jobs?c=engineering&c=data&l=london&l=stockholm&l=remote-emea&l=paris) and [Welcome To The Jungle](https://www.welcometothejungle.com/fr/jobs?page={page_number}&aroundQuery=&query=data%20engineer&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDI&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDD%20%2F%20Temporaire&refinementList%5Bcontract_type_names.fr%5D%5B%5D=Autres&refinementList%5Bcontract_type_names.fr%5D%5B%5D=VIE&refinementList%5Bcontract_type_names.fr%5D%5B%5D=Freelance) where I found my first tech job.

Characteristics:
- Javascript based pages require additional scraping library Playwright
- HTML will eventually change and requires detection as well as manual update of the XPath
- Different websites can show more or less fields (eg. remote policy) which will result in null values
- Schema evolution is not expected
- If a job offer appears on at least 2 scraped websites, how will the duplicate be detected

### Ingestion

The ingestion is made with the Scrapy framework that pulls the web data. It adds a pipeline feature which formats the data into predefined fields and writes into a database in a batch process.

All the ingestion work is encapsulated in one of the two python packages (best practices with Airflow) [data-job-crawler](https://github.com/FelitaD/data-job-crawler).


### Transformation

All transformations are made with Python in a specific ETL pipeline [data-job-etl](https://github.com/FelitaD/data-job-etl).
The processing consist of cleaning and reformatting certain fields and extracting the technology names from the text field into a new column. The data is finally modelled to be loaded in a new database.

### Storage

PostgreSQL is the only type of storage is used accross the whole pipeline due to the non necessity of using NoSQL stores since it has structured data of small size and small read/write workload.

Capacity limitations:
- Relation max size 32 TB
- Field max size 1 GB
- 1600 columns max

Schemas:
- Raw data is a single mega relation
- Processed data is normalized
- Pivotted data is transformed specially for use in Tableau

![img](project_diagrams/de-job-market_diagram.png)

### Orchestration

Following the best practices with Airflow then all the ingestion work is encapsulated in a python package [data-job-crawler](https://github.com/FelitaD/data-job-crawler).

## How to run

Everything was run in development stage locally.  
  
- Install custom packages from pypi  
  - Data ingestion: [data-job-crawler](https://github.com/FelitaD/data-job-crawler)  
  - Data processing: [data-job-etl](https://pypi.org/project/data-job-etl/)  
- Execute `playwright install` to enable playwright library used to scrape Javascript web pages.  
  
- Install Airflow: [installation instructions](https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html)  
   
- Create Postgres database `job_market` with username `JOB_MARKET_DB_USER` and password `JOB_MARKET_DB_PWD` as environment variables.   
  
- Run ```airflow standalone``` to initialise the Airflow database, make a user, and start all components (development phase).<br>  
- Visit Airflow UI `localhost:8080` in the browser and use the admin account details shown on the terminal to login, or username `admin`   
- password in `standalone_admin_password.txt`
  - In the DAGs tab, toggle on job-market-batch. Trigger the DAG manually if it's not running.  
