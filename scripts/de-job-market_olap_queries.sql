select created_at, count(*) as jobs_scraped from raw_jobs group by created_at order by created_at desc;
select created_at, count(*) as jobs_processed from pivotted_jobs group by created_at order by created_at desc;

select * from raw_jobs where created_at = '2023-01-29' and remote LIKE '%total%';

select * from pivotted_jobs where created_at = '2023-01-29' order by title;
select * from pivotted_jobs where created_at = '2023-01-29' and remote LIKE '%total%' order by title;
select * from pivotted_jobs where created_at = '2023-01-29' and remote LIKE '%total%' and title LIKE '%unior%' order by title ;
select * from pivotted_jobs where created_at = '2023-01-29' and remote LIKE '%partiel%' and title LIKE '%unior%' order by title ;

