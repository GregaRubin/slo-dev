from scrappers.base_scrapper import BaseScrapper
from bs4 import BeautifulSoup
from requests import request
from datetime import datetime, timedelta
from utils.job_info import JobInfo
import json

class MojedeloScrapper(BaseScrapper):
    def __init__(self, name: str = "MojedeloScrapper", logfile_name: str = "mojedelo_scrapper.log"):
        super().__init__(name, logfile_name)
        self.base_url = "https://www.mojedelo.com/"
        self.enable_scrape = True
        self.enable_backfill = True
        self.backfill_end_reached = False
        self.backfill_post_limit = 20
        self.scrape_post_limit = 20
        self.oldest_fecthed_date = None
        self.newest_fetched_date = None
        self.backfill_hash_cashe = set()  # To avoid duplicate jobs during backfill
        self.scrape_hash_cashe = set()  # To avoid duplicate jobs during scrape

    def backfill(self) -> list[JobInfo] | None:
        if not self.enable_backfill:
            self.info("Backfill is disabled, skipping backfill.")
            return None
        
        if self.backfill_end_reached:
            self.info("Backfill end reached, no more pages to fetch.")
            return None
        
        jobs = []
        page_num = 1
        
        return jobs


    def load(self):
        try:
            self.info(f"Loading JSON config")
            config_data = self.load_scrapper_config()
            self.enable_scrape = config_data.get("enable_scrape", True)
            self.enable_backfill = config_data.get("enable_backfill", False)
            self.backfill_page_limit = config_data.get("backfill_page_limit", 20)
            oldest_date_str = config_data.get("oldest_fecthed_date", None)
            newest_date_str = config_data.get("newest_fetched_date", None)

            self.oldest_fecthed_date = datetime.strptime(oldest_date_str, '%d. %m. %Y') if oldest_date_str else None
            self.newest_fetched_date = datetime.strptime(newest_date_str, '%d. %m. %Y') if newest_date_str else None
        except Exception as e:
            self.error(f"Error loading JSON config: {e}")

    def save(self):
        try:
            self.info(f"Saving JSON config")
            config_data = {
                "enable_scrape": self.enable_scrape,
                "enable_backfill": self.enable_backfill,
                "backfill_page_limit": self.backfill_page_limit,
                "oldest_fecthed_date": self.oldest_fecthed_date.strftime('%d. %m. %Y') if self.oldest_fecthed_date else None,
                "newest_fetched_date": self.newest_fetched_date.strftime('%d. %m. %Y') if self.newest_fetched_date else None
            }
            self.save_scrapper_config(config_data)
        except Exception as e:
            self.error(f"Error saving JSON config: {e}")


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

    def fetch(self) -> list[JobInfo] | None:
        self.load()
        res_jobs = []
        #todo have a backfill function (10-20 fetches), save oldest date in a file, turn off once you reach end of site pages
        #also save latest date and link to skip already fetched jobs
        self.info(f"Starting {self.name}...")
        a = self.fetch_page_base_info(1)
        b = 0
        self.save()
        pass
