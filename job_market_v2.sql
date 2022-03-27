CREATE TABLE "jobs" (
  "id" SERIAL PRIMARY KEY,
  "title" varchar,
  "company_id" varchar,
  "url" varchar UNIQUE,
  "type" varchar,
  "location" varchar,
  "remote" varchar,
  "language" varchar,
  "technos" list
);

CREATE TABLE "companies" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar UNIQUE,
  "industry" varchar
);

CREATE TABLE "technos" (
  "name" varchar PRIMARY KEY,
  "category" varchar
);

ALTER TABLE "jobs" ADD FOREIGN KEY ("company_id") REFERENCES "companies" ("id");

ALTER TABLE "technos" ADD FOREIGN KEY ("name") REFERENCES "jobs" ("technos");
