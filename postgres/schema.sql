BEGIN;

CREATE TABLE IF NOT EXISTS companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS job_specializations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TYPE seniority_level AS ENUM ('Intern', 'Junior', 'Mid', 'Senior', 'Staff', 'Principal', 'Manager', 'Director');

CREATE TYPE employment_type AS ENUM ('Full-time', 'Part-time', 'Contract', 'Temporary', 'Internship', 'Freelance');

CREATE TYPE work_mode AS ENUM ('Remote', 'Onsite', 'Hybrid');


CREATE TABLE IF NOT EXISTS programming_languages (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS frameworks (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS databases (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS other_tools (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS countries (
    id SERIAL PRIMARY KEY,
    iso2 CHAR(2) NOT NULL UNIQUE,
    iso3 CHAR(3) UNIQUE,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS industries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,

    job_title        VARCHAR(255) NOT NULL,
    company_id       INT NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    job_specialization_id INT REFERENCES job_specializations(id),

    post_timestamp   TIMESTAMPTZ NOT NULL,
    closing_timestamp TIMESTAMPTZ NOT NULL,

    link             TEXT NOT NULL,
    website          TEXT,

    country_id       INT REFERENCES countries(id) ON DELETE SET NULL,
    work_locations   TEXT[],

    seniority        seniority_level,
    years_of_experience INT,
    work_mode        work_mode,
    employment_type  employment_type,
    visa_sponsorship BOOLEAN,
    industry         industries,

    programming_languages INT[],
    frameworks           INT[],
    databases            INT[],
    other_tools           INT[],

    salary_min       NUMERIC,
    salary_max       NUMERIC,

    description      TEXT
);

CREATE INDEX idx_jobs_programming_languages ON jobs USING GIN(programming_languages);
CREATE INDEX idx_jobs_frameworks ON jobs USING GIN(frameworks);
CREATE INDEX idx_jobs_databases ON jobs USING GIN(databases);
CREATE INDEX idx_jobs_other_tools ON jobs USING GIN(other_tools);
CREATE INDEX idx_jobs_post_timestamp ON jobs(post_timestamp);

COMMIT;