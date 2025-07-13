from scrappers.base_scrapper import BaseScrapper
from bs4 import BeautifulSoup
from requests import request
from datetime import datetime, timedelta
from utils.job_info import JobInfo

class MojedeloScrapper(BaseScrapper):
    def __init__(self, name: str = "MojedeloScrapper", logfile_name: str = "mojedelo_scrapper.log"):
        super().__init__(name, logfile_name)
        self.base_url = "https://www.mojedelo.com/"
    
    # returns array of job titles, company name, posting dates, and links
    def fetch_page_base_info(self, page_num: int) -> list[JobInfo] | None:
        try:
            job_results = []
            url = f"{self.base_url}/prosta-delovna-mesta/racunalnistvo-programiranje/vse-regije?p={page_num}"
            res = request("GET", url)
            if res.status_code != 200:
                self.error(f"Failed to fetch page {page_num}: {res.status_code}")
                return None
            
            soup = BeautifulSoup(res.text, 'html.parser')
            jobs = soup.find_all("div", class_="w-inline-block job-ad top w-clearfix")
            for job in jobs:
                link_str = job.find("a", class_="details overlayOnHover1")["href"]
                link_str = self.base_url + link_str

                title_str = job.find("h2", class_ = "title").text.strip()

                time_div = job.find("div", class_="boxItemGroup")
                time_str = time_div.find("div", class_="detail").text.strip()
                if (time_str == "Danes"):
                    date = datetime.now()
                    time_str = date.strftime('%d. %m. %Y')
                elif (time_str == "Včeraj"):
                    date = datetime.now() - timedelta(days=1)
                    time_str = date.strftime('%d. %m. %Y')

                company_div = job.find("div", class_="boxItemGroup boxName")
                company_str = company_div.find("div", class_="detail").text.strip()

                job_results.append(JobInfo(title=title_str, company=company_str, date=time_str, link=link_str, site=self.base_url))

            return job_results

        except Exception as e:
            self.error(f"Error fetching page base info, page {page_num}: {e}")
            return None

    def fetch(self):
        self.info(f"Starting {self.name}...")
        a = self.fetch_page_base_info(1)
        b = 0
        pass
