"""
Decorator which logs the wrapped function/method.

The following are logged:
    1. name of the function called
    2. arg(s) passed for the function called (if any)
    3. kwarg(s) passed for the function called (if any)
    4. execution time of the function called (in seconds)

    * also catches and logs any exceptions raised gracefully.
"""

import time
from functools import partial, wraps

from logbook import Logger

__version__ = "1.1.3"


def iologger(function=None, catch_exceptions=True):
    """
    Decorator which logs the wrapped function/method.

    The following are logged:
        1. name of the function called
        2. arg(s) passed for the function called (if any)
        3. kwarg(s) passed for the function called (if any)
        4. execution time of the function called (in seconds)

        * also catches and logs any exceptions raised gracefully.

    :param catch_exceptions: will catch exceptions gracefully if true.
    :param function: func to run and all its args/kwargs.
    :return: returns func(*args, **kwargs)
    """

    if function is None:
        return partial(iologger, catch_exceptions=catch_exceptions)

    logger = Logger("IOL - {}".format(function.__name__))

    @wraps(function)
    def wrapper(*args, **kwargs) -> None:

        def run_function(func):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()

            logger.info("returned: '{}'".format(result))
            elapsed = end - start
            logger.debug("...Finished ({:f} seconds)".format(elapsed))

            return result

        logger.debug("Starting...")
        arg_dict = dict()
        arg_dict['args'] = args
        arg_dict['kwargs'] = kwargs
        logger.info("passed args/kwargs = {}".format(arg_dict))

        if catch_exceptions:
            with logger.catch_exceptions():
                return run_function(function)
        else:
            return run_function(function)

    return wrapper
