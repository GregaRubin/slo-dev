import logging
import config
from logger import setup_logger
import os
from utils.job_info import JobInfo

class BaseScrapper:
    """
    Base class for scrappers.
    """
    def __init__(self, name, logfile_name):
        file_path = os.path.join(config.LOGGING_PATH, logfile_name)
        self.logger = setup_logger(name, file_path, config.LOGGING_MAX_BYTES, config.LOGGING_MAX_FILES, config.LOGGIN_LEVEL)
        self.name = name
    
    def fetch() -> list[JobInfo] | None:
        raise NotImplementedError("Subclasses must implement this method.")
    
    def send(jobs: list[JobInfo]):
        pass

    def run(self):
        jobs = self.fetch()
        #send(jobs)

    def error(self, message):
        self.logger.error(f"{message}")

    def info(self, message):
        self.logger.info(f"{message}")
    
    def debug(self, message):
        self.logger.debug(f"{message}")
    
    def warning(self, message):
        self.logger.warning(f"{message}")