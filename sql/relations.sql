--- processed_jobs

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

UPDATE processed_jobs AS p1
SET size = r.size, education = r.education, experience = r.experience
FROM raw_jobs AS r
INNER JOIN processed_jobs AS p2 ON p2.id = r.id;

--- pivotted_jobs

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

--- apply

DROP TABLE IF EXISTS apply CASCADE;

CREATE TABLE apply AS
    SELECT p.id AS job_id
    FROM processed_jobs AS p
        WHERE p.title ~* '.*(data|analytics|devops|cloud).*(engineer|ingénieur|ingenieur).*|.*(engineer|ingénieur).*(data|données|donnees|big data|bigdata)|.*etl.*'
        AND p.title !~* '.*(senior|head of|intern|internship|stage|alternance|alternant|apprentice|apprenti).*';

ALTER TABLE "apply" ADD FOREIGN KEY ("job_id") REFERENCES "processed_jobs" ("id");

ALTER TABLE apply
ADD COLUMN open bool;

ALTER TABLE apply
DROP COLUMN open bool;



