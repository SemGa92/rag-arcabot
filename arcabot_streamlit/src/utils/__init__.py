import os
import logging


logging_level = os.getenv('LOGGING_LEVEL', 'INFO')
log_switcher = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
}

logging.basicConfig(level=log_switcher.get(logging_level))
logger = logging.getLogger(__name__)