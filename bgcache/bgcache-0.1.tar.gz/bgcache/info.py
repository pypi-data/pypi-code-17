import logging

from time import time


def info(message=None, count=True):

    def decorator(old_function):
        def new_function(*args, **kwargs):
            msg = old_function.__name__.replace("_", " ").capitalize() if message is None or callable(message) else message
            t_ini = time()
            result = old_function(*args, **kwargs)
            msg = "{}. ({:.2f}s)".format(msg, time() - t_ini)
            if count and hasattr(result, '__len__'):
                msg = "{} ({} items)".format(msg, len(result))
            logging.info("{} [done]".format(msg))
            return result
        return new_function

    # If it's called without parenthesis
    if callable(message):
        return decorator(message)

    return decorator