-- After insert on processed_jobs, insert new row in apply containing the job id
CREATE OR REPLACE FUNCTION create_apply()
   RETURNS TRIGGER
AS $$
BEGIN
    INSERT INTO apply(job_id)
    VALUES(NEW.id);
    RETURN NULL;
END;
$$ LANGUAGE PLPGSQL;

DROP TRIGGER IF EXISTS insert_apply ON processed_jobs;

CREATE TRIGGER insert_apply
    AFTER INSERT ON processed_jobs
    FOR EACH ROW
    EXECUTE FUNCTION create_apply();

-- After insert on apply, update relevant column
CREATE OR REPLACE FUNCTION is_relevant()
   RETURNS TRIGGER
AS $$
BEGIN
    UPDATE apply
    SET relevant = TRUE
    FROM processed_jobs
    WHERE apply.job_id = processed_jobs.id
    AND title ~* '.*(data|analytics|devops|cloud).*(engineer|ingénieur).*|.*(engineer|ingénieur).*(data|données|big data|bigdata)|.*etl.*';
    RETURN NULL;
END;
$$ LANGUAGE PLPGSQL;

DROP TRIGGER IF EXISTS insert_relevance ON apply;

CREATE TRIGGER insert_relevance
    AFTER INSERT ON apply
    FOR EACH ROW
    EXECUTE FUNCTION is_relevant();



