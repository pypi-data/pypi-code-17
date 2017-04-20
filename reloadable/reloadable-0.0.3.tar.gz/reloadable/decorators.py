from functools import wraps
from time import sleep
from reloadable import config


STOP_CONDITION_EXCEPTION = KeyboardInterrupt


def reloadable(exception_callback=lambda e: None, sleep_time: float=0):
    def decorator(func):
        if not config.ENABLED:
            return func

        @wraps(func)
        def wrapper(*args, **kwargs):
            while True:
                try:
                    func(*args, **kwargs)
                except STOP_CONDITION_EXCEPTION as e:
                    raise e
                except Exception as e:
                    exception_callback(e)
                    sleep(sleep_time)
        return wrapper
    return decorator
