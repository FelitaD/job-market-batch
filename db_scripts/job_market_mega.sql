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

insert into mega.jobs values(1, 'http://www.example.com', 'data engineer junior', 'spotify', null, 'permanent', 'music', 'yes', '2022-02-05', 'Text');
insert into mega.jobs values(2, 'http://www.example.com/2', 'data engineer', 'spotify', null, 'permanent', 'music', 'yes', '2022-02-05', 'Text');
insert into mega.jobs values(3, 'http://www.example.com/3', 'data engineer', 'renaissance', null, 'CDI', 'politics', 'partiel', '2022-02-05', 'Text');

select * from mega.jobs;
