import config
from logger import setup_logger
import os
from utils.job_info import JobInfo
import utils.config_utils

class BaseScrapper:
    """
    Base class for scrappers.
    """
    def __init__(self, name, logfile_name):
        logging_folder = utils.config_utils.get_absolute_path(config.LOGGING_PATH)
        file_path = logging_folder + "/" + logfile_name
        self.logger = setup_logger(name, file_path, config.LOGGING_MAX_BYTES, config.LOGGING_MAX_FILES, config.LOGGIN_LEVEL)
        self.name = name
    
    def fetch() -> list[JobInfo] | None:
        raise NotImplementedError("Subclasses must implement this method.")
    
    def send(jobs: list[JobInfo]):
        pass

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