from typing import Optional
from logging import Logger, DEBUG


def log_calculation(logger: Logger, function_name: Optional[str]=None):
    """
    Decorator to log function calls and their results to a specified logger. Useful for debugging helper functions
    of the simulation process.
    :param logger: Logger instance to log to.
    :param function_name: Alternative function name used in log entry.
    :return: Decorated function that logs its calls.
    >>> from io import StringIO
    >>> import logging
    >>> from logging import basicConfig
    >>> log_message = StringIO()
    >>> logger = basicConfig(stream=log_message, level=DEBUG)
    >>> f = log_call(logging)(max)
    >>> f(3, 4)
    4
    >>> log_message.getvalue()
    'DEBUG:root:max(3, 4)=4\\n'
    """
    def wrapper(func):
        name = func.__name__ if not function_name else function_name

        def wrapped(*args):
            result = func(*args)
            logger.log(DEBUG, "{0}({1})={2}".format(name, ', '.join(map(str, args)), result))
            return result
        return wrapped
    return wrapper


def log_function(name: str, log: Logger):
    """
    Decorator that logs function result to specified logger using log level DEBUG, 
    useful for debugging purposes.
    :param name: Human readable name of the function to be logged. 
    :param log: Logger instance to be used for logging.
    :return: Decorated function.
    """
    def wrapper(func):
        def wrapped(*args):
            result = func(*args)
            log.log(DEBUG, "{0}={1}".format(name, result))
            return result
        return wrapped
    return wrapper

