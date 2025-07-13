class JobInfo:
    def __init__(self, title, company, date, link, site):
        self.title = title
        self.company = company
        self.date = date # Ensure date is a string in the format 'dd. mm. yyyy'
        self.link = link
        self.site = site
        self.description = None

    def __repr__(self):
        return f"JobInfo(title={self.title}, company={self.company}, date={self.date}, link={self.link}, site={self.site})"