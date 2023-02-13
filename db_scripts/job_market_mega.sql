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
