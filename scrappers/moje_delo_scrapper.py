import os
from enum import Enum
from datetime import datetime
from scrappers.base_scrapper import BaseScrapper
from utils.job_info import JobInfo
from bs4 import BeautifulSoup
from utils.rate_limit_request import RateLimitedRequester

SLO_LANGUAGE_ID = "db3c58e6-a083-4f72-b30b-39f2127bb18d"
SWE_CATEGORY_ID = "64f003ff-6d8b-4be0-b58c-4580e4eeeb8a"
TENANT_ID = os.getenv("MOJE_DELO_TENANT_ID")
CHANNEL_ID = os.getenv("MOJE_DELO_CHANNEL_ID")

BASE_API_URL = "https://api.mojedelo.com/"
BASE_URL = "https://www.mojedelo.com/"
JOB_LIST_API_URL = BASE_API_URL + "job-ads-search"
JOB_DETAIL_API_URL = BASE_API_URL + "job-ads"
JOB_DETAIL_URL = BASE_URL + "oglas/*/"

REQUEST_COOLDOWN_S = 5.0
PAGE_SIZE = 100

HEADERS = {
    "tenantId": TENANT_ID,
    "channelId": CHANNEL_ID,
    "languageId": SLO_LANGUAGE_ID,
    "Accept": "application/json"
}

class TimeFilter(Enum):
    NEWER_THAN = "newer"
    OLDER_THAN = "older"

class MojeDeloScrapper(BaseScrapper):
    def __init__(self, name: str, enable_backfill: bool, fetch_limit: int, backfill_limit: int, run_interval_seconds: int):
        super().__init__(name, enable_backfill, fetch_limit, backfill_limit, run_interval_seconds)
        self.requests = RateLimitedRequester(REQUEST_COOLDOWN_S)
        self.jobs_cache = None

    def populate_job(self, job_preview: JobInfo) -> bool:
        try:
            url = JOB_DETAIL_API_URL + "/" + job_preview.link.rsplit("/", )[-1]
            res = self.requests.get(url, headers=HEADERS).json()
            translation = res["data"]["jobAdTranslations"][0]
            html_text = translation["title"] + "\n\n" + translation["jobDescription"] + "\n\n" + translation["weOffer"] + "\n\n" + translation["weExpect"]
            soup = BeautifulSoup(html_text, "html.parser")
            job_preview.description = soup.get_text(strip=True)
            return True
        except Exception as e:
            self.error(f"Error: {e}, when populating job: {job_preview}")
            return False
        
    #todo jobs are not chronologically sorted, fetch all, sort locally (newest first)
    def fetch_job_previews_since(self, timestamp: int, time_filter: TimeFilter) -> list[JobInfo]:
        valid_jobs = []
        end_reached = False
        current_job_count = 0
        total_job_count = None

        if not self.jobs_cache:
            while not end_reached:
                    params = {
                        "jobCategoryIds": "64f003ff-6d8b-4be0-b58c-4580e4eeeb8a",
                        "pageSize": PAGE_SIZE,
                        "startFrom": current_job_count
                    }

                    res = self.requests.get(JOB_LIST_API_URL, params=params, headers=HEADERS).json()
                    if total_job_count == None:
                        total_job_count = int(res["data"]["total"])
                    else:
                        if current_job_count >= total_job_count:
                            end_reached = True
                            break
                    
                    items = res["data"]["items"]
                    if len(items) == 0:
                        end_reached = True
                        break
                    else:
                        current_job_count += len(items)
                    
                    for item in items:
                        try:
                            title = item["title"]
                            locations = item.get("town", {}).get("translation") or item.get("jobLocationInput")
                            country = item["country"]["translation"]
                            company = item["company"]["name"]
                            link = JOB_DETAIL_URL + item["id"]
                            iso_time_str = item["startDate"]
                            dt = datetime.fromisoformat(iso_time_str.replace("Z", "+00:00"))
                            ts = int(dt.timestamp())
                            job_info = JobInfo(title, company, ts, link)
                            job_info.website = BASE_URL
                            job_info.country = country
                            job_info.work_locations = locations

                            valid_jobs.append(job_info)
                        except Exception as e:
                            self.error(f"Error: {e}, when parsing job item: {item}")
        
            self.jobs_cache = valid_jobs
        else:
            valid_jobs = self.jobs_cache
    
        if time_filter is TimeFilter.NEWER_THAN:
            valid_jobs = [job for job in valid_jobs if job.post_timestamp >= timestamp]
        elif time_filter is TimeFilter.OLDER_THAN:
            valid_jobs = [job for job in valid_jobs if job.post_timestamp <= timestamp]
        
        valid_jobs.sort(key=lambda job: job.post_timestamp, reverse=True)
        return valid_jobs
    
    def fetch(self, limit: int, existing_job_hashes: set[str], last_fetch_timestamp: int) -> list[JobInfo]:
        populated_jobs = []
        try:
            job_previews = self.fetch_job_previews_since(last_fetch_timestamp, TimeFilter.NEWER_THAN)
            for job_preview in reversed(job_previews):
                if job_preview.hash in existing_job_hashes:
                    continue
                if self.populate_job(job_preview):
                    populated_jobs.append(job_preview)
                if len(populated_jobs) >= limit:
                    break
        except Exception as e:
            self.error(f"Error when fetching and populating content: {e}")
        finally:
            return populated_jobs
    
    def backfill(self, limit: int, existing_job_hashes: set[str], last_backfill_timestamp: int) -> list[JobInfo]:
        populated_jobs = []
        try:
            job_previews = self.fetch_job_previews_since(last_backfill_timestamp, TimeFilter.OLDER_THAN)
            for job_preview in job_previews:
                if job_preview.hash in existing_job_hashes:
                    continue
                self.populate_job(job_preview)
                populated_jobs.append(job_preview)
                if len(populated_jobs) >= limit:
                    break
        except Exception as e:
            self.error(f"Error when fetching backfill content: {e}")
        finally:
            return populated_jobs

    def get_existing_job_hashes(self) -> set[str]:
        #todo check db for existing jobs from mojedelo.com
        return {}