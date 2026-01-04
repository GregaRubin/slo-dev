from logger import setup_logger
import os
import config
from pathlib import Path
from utils.config_utils import get_absolute_path
from dotenv import load_dotenv
from scrappers.moje_delo_scrapper import MojeDeloScrapper

load_dotenv()

SCRAPPERS = [
    MojeDeloScrapper("MojedeloScrapper", False, 10, 50, 600),]

logging_folder = get_absolute_path(config.LOGGING_PATH)
logging_path = os.path.join(logging_folder, "main.log")
logger = setup_logger("main", logging_path, config.LOGGING_MAX_BYTES, config.LOGGING_MAX_FILES)

def run_scrappers():
    scrappers = SCRAPPERS

    for scrapper in scrappers:
        try:
            scrapper.run()
        except Exception as e:
            logger.error(f"Error running {scrapper.name}: {e}")
        else:
            logger.info(f"{scrapper.name} finished.")

if __name__ == "__main__":
    logger.info("Starting scrappers...")
    run_scrappers()
    logger.info("Scrappers finished.")