-- All records processed
select count(*) from raw_jobs;
select count(*) from processed_jobs;
-- Process title
select R.title, P.title from raw_jobs as R join processed_jobs as P on R.id = P.id where R.title != P.title;