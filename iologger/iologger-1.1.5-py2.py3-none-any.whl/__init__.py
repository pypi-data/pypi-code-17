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
from collections import OrderedDict
from functools import partial, wraps
from json import dumps

from logbook import Logger

__version__ = "1.1.5"


def iologger(func=None, catch_exceptions=True):
    """
    Decorator which logs the wrapped function/method.

    The following are logged:
        1. name of the function called
        2. arg(s) passed for the function called (if any)
        3. kwarg(s) passed for the function called (if any)
        4. execution time of the function called (in seconds)

        * also catches and logs any exceptions raised gracefully.

    :param catch_exceptions: will catch exceptions gracefully if true.
    :param func: func to run and all its args/kwargs.
    :return: returns func(*args, **kwargs)
    """

    if func is None:
        return partial(iologger, catch_exceptions=catch_exceptions)

    logger = Logger("iologger[{}]".format(func.__name__))

    @wraps(func)
    def wrapper(*args, **kwargs) -> None:

        def run_function(func):
            func_dict = OrderedDict()
            func_dict.keys = [
                'passed_args',
                'passed_kwargs',
                'returned',
                'exec_time',
                'exception'
            ]

            try:
                func_dict['passed_args'] = args
                func_dict['passed_kwargs'] = kwargs

                start = time.time()
                result = func(*args, **kwargs)
                end = time.time()

                func_dict['returned'] = str(result)
                func_dict['exec_time'] = "{:f}".format(end - start)
                return result
            except Exception as e:
                func_dict['exception'] = str(e)
                raise e
            finally:
                logger.info(dumps(func_dict))

        if catch_exceptions:
            try:
                with logger.catch_exceptions():
                    return run_function(func)
            except Exception as e:
                return e
        else:
            return run_function(func)

    return wrapper
