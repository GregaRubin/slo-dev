import hashlib
class JobInfo:
    def __init__(self, job_title, company, timestamp, link):
        self.job_title = job_title
        self.company = company
        self.post_timestamp = timestamp # unix seconds
        self.link = link
        self.website = None
        self.description = None
        self.country = None
        self.work_locations = None
        self.seniority_level = None
        self.years_of_experience = None
        self.programming_languages = None
        self.frameworks = None
        self.databases = None
        self.other_tools = None
        self.work_mode = None 
        self.salary_min = None
        self.salary_max = None
        self.job_specialization = None
        self.employment_type = None
        self.closing_timestamp = None
        self.visa_sponsorhip = None
        self.industry = None

        self.hash = hashlib.sha256(f"{job_title}{company}{timestamp}{link}".encode("utf-8")).hexdigest()

    def __repr__(self):
        return f"JobInfo(job title={self.job_title}, company={self.company}, timestamp={self.post_timestamp}, link={self.link}, site={self.website})"