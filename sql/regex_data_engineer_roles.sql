--data engineer
--analytics engineer
--ingénieur données
--data ingénieur
--ingénieur data
--ingénieur big data
--ingénieur bigdata
--etl
--devops engineer
--cloud engineer
select title, url
from processed_jobs
where title ~* '.*(data|analytics|devops|cloud).*(engineer|ingénieur).*|.*(engineer|ingénieur).*(data|données|big data|bigdata)|.*etl.*';

