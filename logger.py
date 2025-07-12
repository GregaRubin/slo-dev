import logging
import queue
from logging.handlers import RotatingFileHandler, QueueHandler, QueueListener
from logging import StreamHandler
import os

_log_queue = queue.Queue(-1)

def setup_logger(logfile="app.log", max_bytes=5*1024*1024, backup_count=5, logging_level=logging.DEBUG): 
    if not os.path.exists(os.path.dirname(logfile)):
        os.makedirs(os.path.dirname(logfile))
    
    file_handler = RotatingFileHandler(logfile, maxBytes=max_bytes, backupCount=backup_count)
    console_handler = StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    listener = QueueListener(_log_queue, file_handler, console_handler)
    listener.start()

    root_logger = logging.getLogger()
    root_logger.setLevel(logging_level)
    root_logger.addHandler(QueueHandler(_log_queue))

    return root_logger