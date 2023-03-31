-- Checks how many new jobs were posted
select created_at, count(*) from raw_jobs group by created_at order by created_at desc;
select created_at, count(*) from processed_jobs group by created_at order by created_at desc;