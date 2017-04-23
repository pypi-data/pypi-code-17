#!/usr/bin/env python

import inspect
import logging
import logging.handlers
import os

from enum import IntEnum

class LogHandler(IntEnum):
    Console = 1
    File = 2


def get_named_logger(logger_name, log_level = None):
    ''''''
    logger = logging.getLogger(logger_name)
    if log_level:
        logger.setLevel(log_level)
    return logger


def get_logger(log_level = None):
    ''''''
    frame,filename,line_number,function_name,lines,index = inspect.stack()[1]
    if filename == '<stdin>':
        logger_name = filename
    else:
        resolved_filename = os.path.realpath(filename)
        logger_name = os.path.splitext(os.path.basename(resolved_filename))[0]
    return get_named_logger(logger_name, log_level)


def configure_logger_handlers(
    logger, log_handler_mode, logger_path = None, log_level = logging.INFO,
        overwrite_handlers = True):
    ''''''
    if overwrite_handlers:
        handlers_copy = list(logger.handlers)
        for handler in handlers_copy:
            logger.removeHandler(handler)

    if log_handler_mode & LogHandler.Console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        formatter = '%(asctime)s [%(levelname)s] (%(name)s:%(filename)s) - %(message)s'
        console_handler.setFormatter(logging.Formatter(formatter))
        logger.addHandler(console_handler)

    if log_handler_mode & LogHandler.File:
        file_handler = logging.handlers.RotatingFileHandler(logger_path, maxBytes = 1024*1024, backupCount = 2)
        file_handler.setLevel(log_level)
        formatter = '%(asctime)s [%(levelname)s] (%(name)s:%(filename)s) - %(message)s'
        file_handler.setFormatter(logging.Formatter(formatter))
        logger.addHandler(file_handler)


def initialize_root_logger(
    log_handler_mode, logger_path = None, log_level = logging.INFO):
    ''''''
    root_logger = get_named_logger(None, log_level)
    configure_logger_handlers(root_logger, log_handler_mode, logger_path, log_level)
