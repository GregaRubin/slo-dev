import logging
from scrappers.mojedelo_scrapper import MojedeloScrapper

LOGGING_NAME = "scrapper.log"
LOGGING_PATH = "C:\\dev\\sloDev\\scrapper\\logs"
LOGGING_MAX_BYTES = 50 * 1024 * 1024
LOGGING_MAX_FILES = 10
LOGGIN_LEVEL = logging.DEBUG

SCRAPPERS = [
    MojedeloScrapper(name="MojedeloScrapper"),]