from logger import setup_logger
import os
import config
from scrappers.mojedelo_scrapper import MojedeloScrapper

file_paht = os.path.join(config.LOGGING_PATH, config.LOGGING_NAME)
logger = setup_logger(file_paht, config.LOGGING_MAX_BYTES, config.LOGGING_MAX_FILES, )

def run_scrappers():
    scrappers = config.SCRAPPERS

    for scrapper in scrappers:
        try:
            scrapper.run()
        except Exception as e:
            scrapper.error(f"Error running: {e}")
        else:
            scrapper.info(f"completed successfully.")

if __name__ == "__main__":
    logger.info("Starting scrappers...")
    run_scrappers()
    logger.info("Scrappers finished.")