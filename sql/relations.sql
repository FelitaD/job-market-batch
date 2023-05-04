
CREATE TABLE "processed_jobs" (
  "id" integer PRIMARY KEY,
  "url" varchar(500) UNIQUE NOT NULL,
  "title" varchar(150) NOT NULL,
  "company" varchar(150) NOT NULL,
  "stack" varchar(500) NOT NULL,
  "remote" varchar(150),
  "location" varchar(150),
  "industry" varchar(150),
  "type" varchar(150),
  "created_at" date NOT NULL,
  "text" text NOT NULL
);

ALTER TABLE "processed_jobs" ADD FOREIGN KEY ("id") REFERENCES "raw_jobs" ("id");

CREATE TABLE "pivotted_jobs" (
  "id" SERIAL PRIMARY KEY,
  "raw_id" integer,
  "url" varchar(500) NOT NULL,
  "title" varchar(150) NOT NULL,
  "company" varchar(150) NOT NULL,
  "technos" varchar(500) NOT NULL,
  "remote" varchar(150),
  "location" varchar(150),
  "industry" varchar(150),
  "type" varchar(150),
  "created_at" date NOT NULL
);

DROP TABLE apply CASCADE;

CREATE TABLE apply AS
    SELECT p.id AS job_id
    FROM processed_jobs AS p
        WHERE p.title ~* '.*(data|analytics|devops|cloud).*(engineer|ingénieur|ingenieur).*|.*(engineer|ingénieur).*(data|données|donnees|big data|bigdata)|.*etl.*'
        AND p.title !~* '.*(senior|head of|intern|internship|stage|alternance|alternant|apprentice|apprenti).*';

ALTER TABLE "apply" ADD FOREIGN KEY ("job_id") REFERENCES "processed_jobs" ("id");


ALTER TABLE apply
ADD COLUMN applied_date date;


UPDATE processed_jobs AS p1
SET size = r.size, education = r.education, experience = r.experience
FROM raw_jobs AS r
INNER JOIN processed_jobs AS p2 ON p2.id = r.id;


--- Ranking table

DROP TABLE IF EXISTS ranked_jobs;

CREATE TABLE ranked_jobs AS
    SELECT a.job_id AS job_id
    FROM apply AS a;

ALTER TABLE ranked_jobs
ADD PRIMARY KEY (job_id);

ALTER TABLE ranked_jobs
ADD COLUMN rank float;

ALTER TABLE ranked_jobs
ADD COLUMN remote_num float;

ALTER TABLE ranked_jobs
ADD COLUMN exp_num float;