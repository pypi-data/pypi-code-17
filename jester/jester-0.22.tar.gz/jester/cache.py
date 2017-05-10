from datetime import datetime, timedelta

class CacheItem():

    def __init__(self, value, ttl, date_created=datetime.now()):
        self.value = value
        self.ttl = ttl
        self.date_created = date_created

    def is_expired(self):
        if self.ttl is None:
            return False

        return (((datetime.now() - self.date_created) / timedelta(seconds=1)) > self.ttl)


class Cache:

    def __init__(self, max_size=None):
        self.max_size = max_size
        self.storage = {}

    def get(self, key:str):
        item = self.storage.get(key)
        if item is None or item.is_expired():
            return None

        return item.value

    def put(self, key:str, value, ttl=None):
        item = CacheItem(value, ttl)
        self.storage[key] = item
        return True

    def get_or_else(self, key, _else, ttl=None):
        item = self.get(key)

        if item is None:
            value = _else()
            self.put(key, value, ttl)
            return value

        return item


global_cache = Cache()

def cached(key:str, value, ttl=None):
    return global_cache.get_or_else(key, value, ttl)