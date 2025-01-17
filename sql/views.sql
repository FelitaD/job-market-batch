-- Group jobs by date

CREATE VIEW created_raw AS (
    SELECT created_at, count(*)
    FROM raw_jobs AS r
    GROUP BY created_at
    ORDER BY created_at DESC
);

CREATE VIEW created_processed AS (
    SELECT created_at, count(*)
    FROM processed_jobs AS r
    GROUP BY created_at
    ORDER BY created_at DESC
);

-- Jobs freshly scraped

CREATE VIEW new_raw AS (
    SELECT created_at, id, title, company, url
    FROM raw_jobs
    WHERE created_at = (
        SELECT created_at
        FROM raw_jobs
        ORDER BY created_at DESC limit 1)
    ORDER BY created_at DESC
);

CREATE VIEW new_processed AS (
    SELECT created_at, id, title, company, url, stack, summary
    FROM processed_jobs
    WHERE created_at = (
        SELECT created_at
        FROM processed_jobs
        ORDER BY created_at DESC limit 1)
    ORDER BY created_at DESC
);

CREATE VIEW new_apply AS (
    SELECT created_at, id, title, company, url, stack, summary
    FROM processed_jobs AS p
    JOIN apply AS a
    ON p.id = a.job_id
    WHERE created_at = (
        SELECT created_at
        FROM processed_jobs
        ORDER BY created_at DESC limit 1)
);

-- Data Engineer
CREATE VIEW de AS (
    SELECT created_at, id, title, company, stack, remote, location, industry, type, url, summary
    FROM processed_jobs
    WHERE title ~* '.*(data|analytics|devops|cloud).*(engineer|ingénieur).*|.*(engineer|ingénieur).*(data|données|big data|bigdata)|.*etl.*'
    ORDER BY created_at DESC
);

-- Junior Data Engineer positions
CREATE VIEW junior AS (
    SELECT created_at, id, title, company, stack, remote, location, industry, type, url, summary
    FROM processed_jobs
    WHERE title ~* '.*(data|analytics|devops|cloud).*(engineer|ingénieur).*|.*(engineer|ingénieur).*(data|données|big data|bigdata)|.*etl.*'
    AND title ~* '.*junior.*'
    ORDER BY created_at DESC
);

-- Relevant : join apply and processed_jobs
CREATE VIEW relevant AS (
    SELECT *
    FROM processed_jobs AS p
    JOIN apply AS a
    ON p.id = a.job_id
    AND p.type IN ('Permanent', 'VIE', 'CDI', 'Autres', 'Full Time')
    ORDER BY created_at DESC
);
