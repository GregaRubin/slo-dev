from utils.logger import setup_logger
import config
from dotenv import load_dotenv
from scrappers.moje_delo_scrapper import MojeDeloScrapper

load_dotenv()

SCRAPPERS = [
    MojeDeloScrapper("MojedeloScrapper", False, 5, 50, 10),]

logger = setup_logger("main", config.LOGGING_FOLDER + "/main.log", config.LOGGING_MAX_BYTES, config.LOGGING_MAX_FILES)

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