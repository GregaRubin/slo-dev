from utils.logger import setup_logger
import config
from dotenv import load_dotenv
from scrappers.moje_delo_scrapper import MojeDeloScrapper
from multiprocessing import Process
import time

load_dotenv()

# todo move this to yml/json file
SCRAPPERS = [
    (
        MojeDeloScrapper(
            config.MOJE_DELO_NAME,
            config.MOJE_DELO_BACKFILL,
            config.MOJE_DELO_FETCH_LIMIT,
            config.MOJE_DELO_BACKFILL_LIMIT,
            config.MOJE_DELO_RUN_INTERVAL_MINUTES,
        ),
        config.MOJE_DELO_MAX_RUN_TIME_SECONDS,
    )
]

logger = setup_logger(
    "main",
    config.LOGGING_FOLDER + "/main.log",
    config.LOGGING_MAX_BYTES,
    config.LOGGING_MAX_FILES,
)


def run_scrappers():
    logger.info("Starting scrappers processes ...")
    processes = []
    for scrapper, timeout in SCRAPPERS:
        p = Process(target=scrapper.run)
        logger.info(f"Starting {scrapper.name}")
        p.start()
        processes.append((scrapper, p, timeout))

    logger.info("All scrapper processes started.")
    start = time.monotonic()
    while processes:
        for scrapper, p, timeout in processes[:]:
            if not p.is_alive():
                logger.info(f"{scrapper.name} finished")
                processes.remove((scrapper, p, timeout))
            elif time.monotonic() - start > timeout:
                logger.error(
                    f"{scrapper.name} exceeded timeout {timeout}s, terminating"
                )
                p.terminate()
                processes.remove((scrapper, p, timeout))
        time.sleep(1)


if __name__ == "__main__":
    logger.info("################################################")
    run_scrappers()
    logger.info("################################################")
