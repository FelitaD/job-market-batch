--

select created_at, id, title, company, url from raw_jobs order by created_at desc limit 10;
select created_at, id, title, company, url from pivotted_jobs order by created_at desc limit 10;

select created_at, count(*) as jobs_scraped from raw_jobs group by created_at order by created_at desc;
select created_at, count(*) as jobs_processed from pivotted_jobs group by created_at order by created_at desc;

select * from raw_jobs where created_at = '2023-02-05';
select * from pivotted_jobs where created_at = '2023-02-05' order by title;

-- OLAP

select title, company, technos, remote, url
from pivotted_jobs
where created_at = '2023-01-30'
    and title like '%unior%'
    and (remote like '%total%'
        or remote like '%partiel%')
order by title;

select title, company, remote, url
from raw_jobs
where created_at = '2023-01-30'
    and title like '%unior%'
    and (remote like '%total%'
        or remote like '%partiel%')
order by title;


