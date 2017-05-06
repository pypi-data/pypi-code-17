"""
deliverybot_libs/log.py
~~~~~~~~~~~~~~~~~~~~~~~

Common logging functionality
"""
import logging
from logging.handlers import RotatingFileHandler
import os

DEFAULT_BACKUP_COUNT = 1
DEFAULT_LOG_SIZE = 1024 * 1024 * 50

_formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')


def _get_log_file_path(file_name):
    return os.path.join(settings.logging['directory'], file_name)


def _get_handler(file_name, log_size, log_backup_count):
    handler = RotatingFileHandler(_get_log_file_path(file_name),
                                  maxBytes=log_size,
                                  backupCount=log_backup_count)
    handler.setFormatter(_formatter)
    return handler


def setup_logger(name, file_directory, file_name, log_level,
                 log_size=DEFAULT_LOG_SIZE,
                 log_backup_count=DEFAULT_BACKUP_COUNT):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.addHandler(_get_handler(file_name, log_size, log_backup_count))
