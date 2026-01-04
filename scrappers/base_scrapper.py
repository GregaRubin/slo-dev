import config
from logger import setup_logger
from datetime import datetime, timedelta, timezone
from utils.job_info import JobInfo
import tempfile
from filelock import FileLock
from abc import ABC, abstractmethod
import utils.config_utils

class BaseScrapper(ABC):
    """
    Base class for scrappers.
    """
    def __init__(self, name: str, enable_backfill: bool, fetch_limit: int, backfill_limit: int, run_interval_seconds: int):
        logging_folder = utils.config_utils.get_absolute_path(config.LOGGING_PATH)
        file_path = logging_folder + "/" + name + ".log"
        self.logger = setup_logger(name, file_path, config.LOGGING_MAX_BYTES, config.LOGGING_MAX_FILES, config.LOGGIN_LEVEL)
        self.name = name
        self.enable_backfill = enable_backfill
        self.fetch_limit = fetch_limit
        self.backfill_limit = backfill_limit
        #todo change days to 1
        yesterday = datetime.now(timezone.utc).date() - timedelta(days=10)
        dt_yesterday = datetime.combine(yesterday, datetime.min.time(), tzinfo=timezone.utc)
        self.last_fetch_timestamp = int(dt_yesterday.timestamp())
        self.last_backfill_timestamp = self.last_fetch_timestamp - 1
        self.last_run_timestamp = 0
        self.run_interval_seconds = run_interval_seconds

    # get job postings from last_fetch_date (unix seconds) to newer job postings, should not scrape existing jobs again
    @abstractmethod
    def fetch(self, limit: int, existing_job_hashes: set[str], last_fetch_timestamp) -> list[JobInfo]:
        pass
    
    # get job postings from last_backfill_date (unix seconds) to older job postings, should not scrape existing jobs again
    @abstractmethod
    def backfill(self, limit: int, existing_job_hashes: set[str], last_backfill_timestamp: int) -> list[JobInfo]:
        pass

    # get job posting hashes which already exist in db for this specific website
    @abstractmethod
    def get_existing_job_hashes(self) -> set[str]:
        pass
    
    # todo implement
    def send_to_ingestion_service(self, jobs: list[JobInfo]):
        pass

    def load(self):
        data = self.load_scrapper_config()
        if not data:
            self.info("No saved config found, using defaults.")
            return

        self.enable_backfill = data.get("enable_backfill", self.enable_backfill)
        self.fetch_limit = data.get("fetch_limit", self.fetch_limit)
        self.backfill_limit = data.get("backfill_limit", self.backfill_limit)
        self.last_fetch_timestamp = data.get("last_fetch_timestamp", self.last_fetch_timestamp)
        self.last_backfill_timestamp = data.get("last_backfill_timestamp", self.last_backfill_timestamp)
        self.last_run_timestamp = data.get("last_run_timestamp", self.last_run_timestamp)
        self.run_interval_seconds = data.get("run_interval_seconds", self.run_interval_seconds)

        self.info(f"Loaded scrapper config: {data}")


    def save(self):
        data = {
            "enable_backfill": self.enable_backfill,
            "fetch_limit": self.fetch_limit,
            "backfill_limit": self.backfill_limit,
            "last_fetch_timestamp": self.last_fetch_timestamp,
            "last_backfill_timestamp": self.last_backfill_timestamp,
            "last_run_timestamp": self.last_run_timestamp,
            "run_interval_seconds": self.run_interval_seconds,
        }

        self.save_scrapper_config(data)
        self.info(f"Saved scrapper config: {data}")


    def load_scrapper_config(self):
        try:
            config_path = utils.config_utils.get_absolute_path(config.SCRAPPER_CONFIG_PATH) + "/" + self.name + ".json"
            return utils.config_utils.load_json_file(config_path)
        except Exception as e:
            self.error(f"Error loading scrapper config: {e}")
            return None
        
    def save_scrapper_config(self, data: dict):
        try:
            config_path = utils.config_utils.get_absolute_path(config.SCRAPPER_CONFIG_PATH) + "/" + self.name + ".json"
            utils.config_utils.save_json_file(config_path, data)
        except Exception as e:
            self.error(f"Error saving scrapper config: {e}")

    def run(self):
        try:
            lock = FileLock(f"{tempfile.gettempdir()}/{self.name}.lock")
            with lock.acquire(timeout=1):
                self.load()
                
                now_ts = int(datetime.now(timezone.utc).timestamp())
                if now_ts - self.last_run_timestamp < self.run_interval_seconds:
                    return

                existing_hashes = self.get_existing_job_hashes()
                #todo update last fetch date
                new_jobs = self.fetch(self.fetch_limit, existing_hashes, self.last_fetch_timestamp)

                if self.enable_backfill:
                    old_jobs = self.backfill(self.backfill_limit, existing_hashes, self.last_backfill_timestamp)
                    oldest_date = self.last_backfill_date
                    for job in old_jobs:
                        oldest_date = min(job.date, oldest_date)

                    self.last_backfill_date = oldest_date
                    new_jobs += old_jobs

                self.send_to_ingestion_service(new_jobs)
                self.last_run_timestamp = now_ts
                self.save()            
        except Exception as e:
            self.error(f"Error running scrapper: {e}")

    def error(self, message):
        self.logger.error(f"{message}")

    def info(self, message):
        self.logger.info(f"{message}")
    
    def debug(self, message):
        self.logger.debug(f"{message}")
    
    def warning(self, message):
        self.logger.warning(f"{message}")