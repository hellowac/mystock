import os
import sys
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler


def initializeLogger(
    name: str,
    logfile: str,
    log_level: int = logging.DEBUG,
    file_level: int = logging.INFO,
):

    logger = logging.getLogger(name)

    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter(
        "[%(asctime)s] - %(levelname)s in %(pathname)s:%(lineno)d - %(message)s"
    )
    logger.setLevel(log_level)

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(formatter)
    consoleHandler.setLevel(log_level)
    logger.addHandler(consoleHandler)

    rotatingFileHanlder = RotatingFileHandler(
        f"{logfile}.{datetime.utcnow().strftime('%Y%m%d')}.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=1,
    )
    rotatingFileHanlder.setFormatter(formatter)
    rotatingFileHanlder.setLevel(file_level)
    logger.addHandler(rotatingFileHanlder)

    return logger


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ROOT_LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(ROOT_LOG_DIR, exist_ok=True)

logger = initializeLogger("mystock", os.path.join(ROOT_LOG_DIR, "rootlog"))
