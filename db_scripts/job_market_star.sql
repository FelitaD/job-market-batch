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
