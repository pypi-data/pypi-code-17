from logging import Logger, DEBUG


def log_function(name: str, log: Logger):
    def wrapper(func):
        def wrapped(*args):
            result = func(*args)
            log.log(DEBUG, "{0}={1}".format(name, result))
            return result
        return wrapped
    return wrapper

