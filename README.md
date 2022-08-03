# Data Engineering Job Market

## Description
This project is aimed at building a pipeline while discovering the tools used in data engineering. 
The data being processed is data engineering jobs openings in Europe scraped from different websites.

## Architecture

1. Python crawler
2. PostgreSQL / MongoDB database

[Database diagram](https://dbdiagram.io/d/623f46d0bed618387302d39e)
![](job_market_v2.png)

## Running with Airflow

### Locally
- Change airflow home in bash/zsh profile

```export AIRFLOW_HOME=/Users/donor/PycharmProjects/job-market-batch/airflow```

- Install Airflow using the constraints file

```AIRFLOW_VERSION=2.3.3```

```PYTHON_VERSION="$(python3 --version | cut -d " " -f 2 | cut -d "." -f 1-2)"```

For example: 3.7

```CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"```

For example: https://raw.githubusercontent.com/apache/airflow/constraints-2.3.3/constraints-3.7.txt

```pip3 install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"```

- The Standalone command will initialise the database, make a user, and start all components for you.

```airflow standalone```

- Visit localhost:8080 in the browser and use the admin account details shown on the terminal to login.

### Docker + project on host




## Details

### 1. Python crawler
Crawler using scrapy framework. Different spiders scrape data from job websites (DatAI, WTTJ, Linkedin...).
Scrapy's Item Pipeline stores data into a PostgreSQL database.

### 2. PostgreSQL database
The database *job_market* contains at first one table *jobs*.
The columns are id (serial), url (unique), title (not null), company, location, type, industry and text.

### 3. Automation with cron jobs
Scripts contain execution of spiders. They are then scheduled with crontab.

### 4.a Streamlined ingestion with Pandas
Read from database to do same basic queries as in psql but with pandas.

### 4.b Synchronization PostgreSQL - Elasticsearch with Logstash
The data that would be the more interesting to analyse is contained in the job openings' text.
For this, Elasticserch will allow us to do some analytics and particularly aggregation of the most frequent terms.
The main goal is to know which technologies are the most in demand for Data Engineer positions in France / Europe.

