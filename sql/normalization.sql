-- Start with mega relation
CREATE SCHEMA IF NOT EXISTS "mega";

CREATE TABLE "mega"."jobs" (
  "id" integer PRIMARY KEY,
  "url" varchar(500) UNIQUE,
  "title" varchar(100),
  "company" varchar(100),
  "location" varchar(100),
  "type" varchar(100),
  "industry" varchar(100),
  "remote" varchar(100),
  "created_at" date,
  "text" text
);

-- Normalize
CREATE SCHEMA IF NOT EXISTS "star";

CREATE TABLE "star"."job" (
  "id" integer PRIMARY KEY,
  "title" varchar(100) NOT NULL,
  "company_id" integer,
  "type" varchar(100),
  "location" varchar(100),
  "remote" varchar(100),
  "url" varchar(500) UNIQUE,
  "text" text NOT NULL,
  "created_at" date NOT NULL
);

CREATE TABLE "star"."company" (
  "id" integer PRIMARY KEY,
  "name" varchar(100) UNIQUE,
  "industry_id" integer
);

CREATE TABLE "star"."industry" (
  "id" integer PRIMARY KEY,
  "name" varchar(100) UNIQUE
);

CREATE TABLE "star"."techno" (
  "id" integer PRIMARY KEY,
  "name" varchar(100) UNIQUE
);

CREATE TABLE "star"."job_techno" (
  "job_id" integer,
  "techno_id" integer,
  PRIMARY KEY ("job_id", "techno_id")
);

CREATE INDEX "Date" ON "star"."job" ("created_at");

CREATE UNIQUE INDEX ON "star"."job" ("title", "company_id", "created_at");

ALTER TABLE "star"."job" ADD FOREIGN KEY ("company_id") REFERENCES "star"."company" ("id");

ALTER TABLE "star"."company" ADD FOREIGN KEY ("industry_id") REFERENCES "star"."industry" ("id");

ALTER TABLE "star"."job_techno" ADD FOREIGN KEY ("job_id") REFERENCES "star"."job" ("id");

ALTER TABLE "star"."job_techno" ADD FOREIGN KEY ("techno_id") REFERENCES "star"."techno" ("id");


-- Test with some data
insert into star.industry values(15, 'Entertainement');
insert into star.industry values(3, 'Nuclear');

insert into star.company values(0, 'Spotify', 15);

insert into star.job values(1, 'de', 0, 'CDI', 'Barcelone', 'yes', 'http://greatjob.com', 'You will create pipelines', '2022-10-10');
insert into star.job values(2, 'de', 0, 'CDD', 'Paris', 'no', 'url.com', 'why not', '2023-01-01');
insert into star.job values(2, 'de', 0, 'CDD', 'Paris', 'no', 'url.com', 'why not', '2023-01-01');

select * from star.industry as ind
join star.company as com on ind.id = com.industry_id
join star.job as job on job.company_id = com.id;

truncate star.industry cascade;
