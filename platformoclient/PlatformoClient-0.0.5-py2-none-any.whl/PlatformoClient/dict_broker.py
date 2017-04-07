# -*- coding: utf-8 -*-

from base_broker import BaseBroker


class DictBroker(BaseBroker):
    def __init__(self):
        self.dict = dict()


    def put(self, key, value):
        self.dict[key] = value


    def get(self, key, default=None):
        if self.contain(key):
            return self.dict[key]
        else:
            return default


    def contain(self, key):
        return key in self.dict
