# Data Engineering Job Market

## Description
Pipeline processing data on data engineering job market in Europe.

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

