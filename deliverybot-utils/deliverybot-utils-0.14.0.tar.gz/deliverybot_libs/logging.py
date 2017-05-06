"""
deliverybot_libs/logging.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Common logging functionality
"""
import logging
from logging.handlers import RotatingFileHandler
import os

DEFAULT_BACKUP_COUNT = 1
DEFAULT_LOG_SIZE = 1024 * 1024 * 50

_formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')


def _get_log_file_path(name, log_settings):
    return os.path.join(log_settings['directory'], name)


def _get_handler(name, log_settings):
    handler = RotatingFileHandler(_get_log_file_path(name, log_settings),
                                  maxBytes=log_settings['size'],
                                  backupCount=log_settings['backup'])
    handler.setFormatter(_formatter)
    return handler


def setup_logger(name, log_settings):
    logger = logging.getLogger(name)
    logger.setLevel(log_settings['level'])
    logger.addHandler(_get_handler(name, log_settings))
