import logging
import os

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Info handler
    info_handler = logging.FileHandler("info.log")
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

    # Error handler
    error_handler = logging.FileHandler("error.log")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

    # Remove default handlers
    logger.handlers = []
    # Add handlers
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)


setup_logging()

logger = logging.getLogger(__name__)