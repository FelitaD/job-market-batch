CREATE SCHEMA IF NOT EXISTS "doc";

CREATE TABLE "doc"."jobs" (
  "id" integer PRIMARY KEY,
  "url" varchar UNIQUE,
  "title" varchar,
  "company_id" integer,
  "location_id" integer,
  "remote" boolean,
  "language" varchar,
  "type" varchar,
  "text" varchar,
  "created_at" timestamp
);

CREATE TABLE "doc"."technos" (
  "id" integer PRIMARY KEY,
  "name_pretty" varchar UNIQUE,
  "name_lower" varchar UNIQUE,
  "category_id" integer
);

CREATE TABLE "doc"."aliases" (
  "id" integer PRIMARY KEY,
  "techno_id" integer,
  "alias" varchar
);

CREATE TABLE "doc"."jobs_technos" (
  "job_id" integer,
  "techno_id" integer,
  PRIMARY KEY ("job_id", "techno_id")
);

CREATE TABLE "doc"."categories" (
  "id" integer PRIMARY KEY,
  "category_1" varchar UNIQUE,
  "category_2" varchar UNIQUE,
  "pipeline_phase" varchar UNIQUE,
  "open_source" boolean
);

CREATE TABLE "doc"."companies" (
  "id" integer PRIMARY KEY,
  "name" varchar UNIQUE,
  "industry_id" integer
);

CREATE TABLE "doc"."industries" (
  "id" integer PRIMARY KEY,
  "name" varchar UNIQUE
);

CREATE TABLE "doc"."locations" (
  "id" integer PRIMARY KEY,
  "city" varchar,
  "country" varchar
);

ALTER TABLE "doc"."jobs" ADD FOREIGN KEY ("company_id") REFERENCES "doc"."companies" ("id");

ALTER TABLE "doc"."jobs" ADD FOREIGN KEY ("location_id") REFERENCES "doc"."locations" ("id");

ALTER TABLE "doc"."technos" ADD FOREIGN KEY ("category_id") REFERENCES "doc"."categories" ("id");

ALTER TABLE "doc"."aliases" ADD FOREIGN KEY ("techno_id") REFERENCES "doc"."technos" ("id");

ALTER TABLE "doc"."jobs_technos" ADD FOREIGN KEY ("job_id") REFERENCES "doc"."jobs" ("id");

ALTER TABLE "doc"."jobs_technos" ADD FOREIGN KEY ("techno_id") REFERENCES "doc"."technos" ("id");

ALTER TABLE "doc"."companies" ADD FOREIGN KEY ("industry_id") REFERENCES "doc"."industries" ("id");
