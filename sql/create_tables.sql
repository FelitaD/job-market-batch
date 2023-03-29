
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