import functools
import time

from flask import logging

logger = logging.getLogger(__name__)


def exec_time(func):
    """
    记录函数执行时间
    :param func: 
    :return: 
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        time_diff = (time.time() - start) * 1000
        logger.warning('- 执行{module}.{name}()消耗时间:{time}ms -'
                       .format(module=func.__module__,
                               name=func.__name__,
                               time=float('%.3f' % time_diff))
                       )
        return result

    return wrapper
