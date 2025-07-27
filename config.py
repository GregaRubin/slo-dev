import logging
from scrappers.mojedelo_scrapper import MojedeloScrapper

LOGGING_PATH = "logs"
LOGGING_MAX_BYTES = 50 * 1024 * 1024
LOGGING_MAX_FILES = 10
LOGGIN_LEVEL = logging.DEBUG
SCRAPPER_CONFIG_PATH = "scrapper_configs"

SCRAPPERS = [
    MojedeloScrapper(name="MojedeloScrapper"),]