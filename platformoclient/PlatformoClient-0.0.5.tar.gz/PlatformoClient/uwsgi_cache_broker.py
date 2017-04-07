# -*- coding: utf-8 -*-

from base_broker import BaseBroker


class UwsgiCacheBroker(BaseBroker):
    def __init__(self, cache='platformo_client', expires=0):
        self.cache = cache
        self.expires = expires

        try:
            import uwsgi
            self.uwsgi = uwsgi
        except ImportError as error:
            raise error
        else:
            self.put('cache_valid', 'valid')
            if self.get('cache_valid') != 'valid':
                raise 'The uwsgi cache is missing, please add options "--cache2 name=platformo_client,items=100'

    def put(self, key, value):
        if self.contain(key):
            self.uwsgi.cache_update(key, value, self.expires, self.cache)
        else:
            self.uwsgi.cache_set(key, value, self.expires, self.cache)


    def get(self, key, default=None):
        if self.contain(key):
            return self.uwsgi.cache_get(key, self.cache)
        else:
            return default


    def contain(self, key):
        return self.uwsgi.cache_exists(key, self.cache)
