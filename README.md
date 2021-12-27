# Data Engineering Job Market

## Description
This project is aimed at building a pipeline while discovering the tools used in data engineering. 
The data being processed is data engineering jobs openings in Europe scraped from different websites.

## Architecture

1. Python crawler
2. PostgreSQL / MongoDB database

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

