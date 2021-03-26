DROP TABLE IF EXISTS job_listings;
CREATE TABLE home_joblistings (
    id int primary key auto_increment,
    job_id varchar(1000) DEFAULT 'N/A',
    job_topic varchar(1000) DEFAULT 'N/A',
    company_name varchar(100) DEFAULT 'N/A',
    job_link varchar(1000) DEFAULT 'N/A',
    job_title varchar(1000) DEFAULT 'N/A',
    job_description varchar(5000) DEFAULT 'N/A',
    job_requirements varchar(1000) DEFAULT 'N/A',
    job_location varchar(1000) DEFAULT 'N/A',
    job_salary varchar(1000) DEFAULT 'N/A',
    job_qualification varchar(1000) DEFAULT 'N/A',
    job_type varchar(1000) DEFAULT 'N/A',
    job_experience varchar(1000) DEFAULT 'N/A'
);
