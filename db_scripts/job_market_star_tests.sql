insert into star.industry values(15, 'Entertainement');
insert into star.industry values(3, 'Nuclear');

insert into star.company values(0, 'Spotify', 15);

insert into star.job values(1, 'de', 0, 'CDI', 'Barcelone', 'yes', 'http://greatjob.com', 'You will create pipelines', '2022-10-10');
insert into star.job values(2, 'de', 0, 'CDD', 'Paris', 'no', 'url.com', 'why not', '2023-01-01');
insert into star.job values(2, 'de', 0, 'CDD', 'Paris', 'no', 'url.com', 'why not', '2023-01-01');

select * from star.industry as ind
join star.company as com on ind.id = com.industry_id
join star.job as job on job.company_id = com.id;

truncate star.industry cascade;
