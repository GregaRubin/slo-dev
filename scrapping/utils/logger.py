import logging
import queue
from logging.handlers import RotatingFileHandler, QueueHandler, QueueListener
from logging import StreamHandler
import os

def setup_logger(name, log_file="app.log", max_bytes=5*1024*1024, backup_count=5, logging_level=logging.DEBUG): 
    if not os.path.exists(os.path.dirname(log_file)):
        os.makedirs(os.path.dirname(log_file))

    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(logging_level)

    if not logger.handlers:
        file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        console_handler = logging.StreamHandler()

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger