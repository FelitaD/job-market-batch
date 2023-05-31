# Data Engineering Job Market

Ingest, process, analyse and recommend new data engineer jobs from [Welcome to the Jungle website](https://www.welcometothejungle.com/fr/jobs?query=data%20engineer&page=1). 

**Background**

The initial problem for this project was to filter and analyse jobs based on technologies.  
Data engineering can be technology-centered, but the focus of this project is to apply Platform and Pipeline concepts and best practices, 
using O'Reilly *Fundamentals of Data Engineering* as a reference. 
Below is the final Data Flow of the project.

[Data Flow Miro board](https://miro.com/welcomeonboard/NUtFWUhHSTRoNU1uZG5IZVFBbFl1cUh1VXN4bGUxMmJkR3ZwNVNPa05nMHZRT1c3WWZ1a1JSR2hUd2lzdm1oanwzMDc0NDU3MzYxNTA0MTQ0MjcwfDI=?share_link_id=594368920393)
![Mind map](https://github.com/FelitaD/job-market-batch/blob/main/docs/Mind%20Map.jpg)

**Summary**

- [Architecture](#architecture)
- [Running the project](#running-the-project)
- [Testing the project](#testing-the-project)
  - [End-to-end tests](#end-to-end-tests)
  - [Data quality testing](#data-quality-testing)
  - [Unit testing](#unit-testing)
- [Pipelines](#pipelines)
  - [Ingestion pull pipeline](#ingestion-pull-pipeline)
  - [ETL pipeline](#etl-pipeline)
  - [API pipeline](#api-pipeline)
- [Data Lifecycle](#data-lifecycle)
  - [Source System](#source-system)
  - [Ingestion](#ingestion)
  - [Transformation](#transformation)
  - [Serving](#serving)
  - [Storage](#storage)
  - [Orchestration](#orchestration)


****

## Architecture

A minimal pipeline using Python, Postgres, Airflow and Tableau.

![img](docs/data_lifecycle.jpg)

C4 model diagrams: https://structurizr.com/workspace/79499/diagrams

## Running the project

**Prerequesites**

- Setup environment 
  - Activate venv and install requirements
  - Execute `playwright install` to download chromium
- Install Airflow with pypi: [official instructions](https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html)
- Create `job_market` database and export environment variables `JOB_MARKET_DB_USER` and `JOB_MARKET_DB_PWD`   

**Run locally**

- ```airflow standalone``` will initialise Airflow database, make a user, and start all components (development phase).<br>  
- Airflow UI is at `localhost:8080` with username `admin` and password in `standalone_admin_password.txt`
- In DAGs tab, toggle on job-market-batch and trigger manually if not running.  

## Testing the project

For individual pipelines tests see their respective repositories.

### Airflow Tests

Multiple errors can arise using Airflow. 
The recommended order for testing is the DAG file then individual tasks and backfill taking account of dependencies.
- DAG file
`python3 job_market_etl_dag.py`
- Import time `time python3 job_market_etl_dag.py` (default max 30 seconds) 
- DAG loading `pytest tests/`
- List tasks and test them individually
  - `airflow tasks list job-market-batch`
  - `airflow tasks test job-market-batch TASK 2022-01-01`
- Backfill `airflow dags backfill job-market-batch --start-date 2023-01-01`

### End-to-end Test

- Look at latest job posting
- Query `processed_jobs` table and compare results

Example output :

![img.png](docs/output_junior_view.png)

As seen in the 2nd record above, the job offer isn't for a data engineer. 
Data quality is the goal of the next section.

### Data Quality Testing

- All technologies must be present 
  - Some technologies are written differently (eg. Google BigQuery, Google Big Query)
  - Have to be added manually in `config/definitions.py` from the ETL package
- Eliminate non data engineer jobs
  - About half the jobs despite the filters
  - Verify data engineer roles with `regex_data_engineer_roles.sql`
- Eliminate duplicate jobs 
  - Some jobs are reposted multiple times and have a different url each time
  - Removed by removing the last part of the url, see: `sql/truncate_urls.sql`
- Processing errors
  - To be added in the unit tests input
  - Some queries to spot error in `tests/processing_errors.sql` 
- Missing values
  - Only id, url, title and company have the `NOT NULL` constraint
  - Check other fields in `tests/missing_values.sql`

### Unit Testing

Pytest
- Crawler coverage
- ETL coverage

## Pipelines

### Ingestion pull pipeline

[data-job-crawler](https://github.com/FelitaD/data-job-crawler) 

![img](docs/ingestion_data_flow.jpg)

A first spider designed to parse Javascript pages gathers links to job postings. 
They are stored in S3 then fed to a 2nd spider. 
The final scraped items go through a pipeline writing into Postgres.
Can be scaled with more websites.

### ETL pipeline

[data-job-etl](https://github.com/FelitaD/data-job-etl)

![img](docs/etl_pipeline.jpg)

### API pipeline

[data-job-api](https://github.com/FelitaD/data-job-api)


## Data Lifecycle

### Source system

The data sources are the web pages containing results for the latest data engineering jobs.  The project started with [Spotify](https://www.lifeatspotify.com/jobs?c=engineering&c=data&l=london&l=stockholm&l=remote-emea&l=paris) and [Welcome To The Jungle](https://www.welcometothejungle.com/fr/jobs?page={page_number}&aroundQuery=&query=data%20engineer&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDI&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDD%20%2F%20Temporaire&refinementList%5Bcontract_type_names.fr%5D%5B%5D=Autres&refinementList%5Bcontract_type_names.fr%5D%5B%5D=VIE&refinementList%5Bcontract_type_names.fr%5D%5B%5D=Freelance) where I found my first tech job.

Characteristics:
- Javascript based pages require additional scraping library Playwright
- HTML will eventually change and requires detection as well as manual update of the XPath
- Different websites can show more or less fields (eg. remote policy) which will result in null values
- Schema evolution can occur
- If a job offer appears on at least 2 scraped websites, need to deal with duplicate

### Ingestion

The ingestion is made with Scrapy framework which adds a pipeline feature that conform the data into predefined fields and writes them to the database.

### Transformation

All transformations are made with Python in a specific ETL pipeline [data-job-etl](https://github.com/FelitaD/data-job-etl).
The processing consists of cleaning and reformatting fields and extracting the technology names from the text field into a new column. The data is finally modelled to be loaded in a new database.

### Storage

PostgreSQL is used as OLTP and OLAP stores. The data is uniformely structured with a small read and write workload.

#### Schema 

The raw data is stored in a mega relation. The field `text` is the biggest but should not reach the 1 GB capacity limitation. 
Once transformed, the data is loaded in a new table without normalization. A future implementation would differentiate 2 databases with the schemas:

[Db diagram](https://dbdiagram.io/d/63dfb687296d97641d7e8b0f)

![schema](docs/db_schema.png))

### Orchestration

Airflow is run locally. Following best practices, the custom code is encapsulated in python packages then imported in the DAG.


[Back to top](#data-engineering-job-market)