-- After insert on processed_jobs, insert new row in apply containing the job id
CREATE OR REPLACE FUNCTION create_apply()
   RETURNS TRIGGER
AS $$
BEGIN
    INSERT INTO apply(job_id)
        SELECT NEW.id
        WHERE NEW.title ~* '.*(data|analytics|devops|cloud).*(engineer|ingénieur|ingenieur).*|.*(engineer|ingénieur).*(data|données|donnees|big data|bigdata)|.*etl.*'
        AND NEW.title !~* '.*(senior|head of|intern|internship|stage|alternance|alternant|apprentice|apprenti).*';
    RETURN NULL;
END;
$$ LANGUAGE PLPGSQL;

DROP TRIGGER IF EXISTS insert_apply ON processed_jobs;

CREATE TRIGGER insert_apply
    AFTER INSERT ON processed_jobs
    FOR EACH ROW
    EXECUTE FUNCTION create_apply();
