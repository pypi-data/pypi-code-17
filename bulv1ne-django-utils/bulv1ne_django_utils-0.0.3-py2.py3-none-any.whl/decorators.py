from functools import wraps

from django.core.cache import cache


class cache_function:
    def __init__(self, timeout, key=None):
        self.timeout = timeout
        self.key = key

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = self.key or func.__qualname__
            if callable(key):
                key = key(*args, **kwargs)
            data = cache.get(key)
            if data:
                return data
            data = func(*args, **kwargs)
            cache.set(key, data, self.timeout)
            return data
        return wrapper
