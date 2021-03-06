import logging
import logging.handlers
from concurrent_log_handler import ConcurrentRotatingFileHandler
from logging import *
from datetime import *



def initLogging(file):
    

    logger = logging.getLogger(file)
    logger.setLevel(logging.DEBUG)

    rht = ConcurrentRotatingFileHandler(file, 'a' ,encoding='utf-8')
    fmt = logging.Formatter("%(asctime)s - %(pathname)s - %(funcName)s - %(lineno)s - %(levelname)s : %(message)s", "%Y-%m-%d %H:%M:%S")
    rht.setFormatter(fmt)
    logger.addHandler(rht)
    return logger

