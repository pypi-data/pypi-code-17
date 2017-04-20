from functools import wraps
from time import sleep
from reloadable import config


def reloadable(exception_callback=lambda e: None, sleep_time: float=0,
               stop_condition_exception: BaseException=None):
    def decorator(func):
        if not config.ENABLED:
            return func

        @wraps(func)
        def wrapper(*args, **kwargs):
            while True:
                try:
                    func(*args, **kwargs)
                except (stop_condition_exception or config.STOP_CONDITION_EXCEPTION) as e:
                    raise e
                except Exception as e:
                    exception_callback(e)
                    sleep(sleep_time)
        return wrapper
    return decorator
