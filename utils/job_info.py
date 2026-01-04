import hashlib
class JobInfo:
    def __init__(self, job_title, company, timestamp, link, website, country, locations, description):
        self.job_title = job_title
        self.company = company
        self.post_timestamp = timestamp # unix seconds
        self.link = link
        self.website = website
        self.description = description
        self.country = country
        self.locations = locations
        self.hash = hashlib.sha256(f"{job_title}{company}{timestamp}{link}".encode("utf-8")).hexdigest()

    def __repr__(self):
        return f"JobInfo(job title={self.job_title}, company={self.company}, timestamp={self.post_timestamp}, link={self.link}, site={self.website})"