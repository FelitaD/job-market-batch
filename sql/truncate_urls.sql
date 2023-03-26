-- Remove url as primary key

ALTER TABLE raw_jobs DROP CONSTRAINT jobs_url_key;

-- Truncate urls

UPDATE raw_jobs
SET url = (select split_part(url, '?q=', 1))
WHERE url LIKE '%?q=%';

-- Check for duplicate urls

CREATE VIEW duplicate AS (
    SELECT url, count(url)
    FROM raw_jobs
    GROUP BY (url)
    HAVING count(url) > 1
);

-- Delete rows with same url

DELETE FROM raw_jobs AS a
USING raw_jobs AS b
WHERE a.id < b.id
AND a.url = b.url;

-- Check view again

-- Check for other duplicates
-- unique urls = 4765
-- unique text = 4158
-- unique title, company = 3767
-- unique title, company, created_at = 4257
-- unique title, company, industry, location, type) = 4326
-- unique title, company, location, type, industry, remote, text = 4555
-- unique title, company, location, type, industry, remote, created_at = 4587
-- unique title, company, location, type, industry, remote = 4405

select id, count(distinct(title, company, location, type, industry, remote, created_at))
from raw_jobs group by (title, company, location, type, industry, remote, created_at)
having count(distinct(title, company, location, type, industry, remote, created_at)) > 1;

-- Add primary key
ALTER TABLE raw_jobs ADD PRIMARY KEY (url);