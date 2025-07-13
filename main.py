from logger import setup_logger
import os
import config
from scrappers.mojedelo_scrapper import MojedeloScrapper

file_path = os.path.join(config.LOGGING_PATH, "main.log")
logger = setup_logger("main" ,file_path, config.LOGGING_MAX_BYTES, config.LOGGING_MAX_FILES)

def run_scrappers():
    scrappers = config.SCRAPPERS

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