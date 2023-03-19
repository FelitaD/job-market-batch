# Data Engineering Job Market


- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Testing](#testing)
- [Data Lifecycle](#data-lifecycle)
  - [Source System](#source-system)
  - [Ingestion](#ingestion)
  - [Transformation](#transformation)
  - [Serving](#serving)
  - [Storage](#storage)
  - [Orchestration](#orchestration)

## Project Overview

The purpose of this project is to have a better idea of the data engineering job market. 
The initial goal was to answer certain questions for my job hunt in order to skill up in the right areas. For example, what technologies are the most used by companies in Europe ? What data stack is the most asked for Junior positions ? Etc. 

## Architecture

![img](project_diagrams/data_lifecycle.jpg)

## Testing


## Data Lifecycle

### Source system

The data sources are the web pages containing results for the latest data engineering jobs.  The project started with [Spotify](https://www.lifeatspotify.com/jobs?c=engineering&c=data&l=london&l=stockholm&l=remote-emea&l=paris) and [Welcome To The Jungle](https://www.welcometothejungle.com/fr/jobs?page={page_number}&aroundQuery=&query=data%20engineer&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDI&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDD%20%2F%20Temporaire&refinementList%5Bcontract_type_names.fr%5D%5B%5D=Autres&refinementList%5Bcontract_type_names.fr%5D%5B%5D=VIE&refinementList%5Bcontract_type_names.fr%5D%5B%5D=Freelance) where I found my first tech job.

Characteristics :
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

Capacity limitations :
- Relation max size 32 TB
- Field max size 1 GB
- 1600 columns max

Schemas :
- Raw data is a single mega relation
- Processed data is normalized
- Pivotted data is transformed specially for use in Tableau

### Orchestration

Airflow coordinates the workflow of the ingestion through the transformation. As mentioned earlier, the custom Python code has been packaged then imported in the DAG to follow best practices. The downside is the need to make a release each time the code changes. 
