# -*- coding: utf-8 -*-
from __future__ import absolute_import

"""
Package Description
mongodb manager
robomongo-1.0.0-rc1-darwin-x86_64-496f5c2.dmg

"""
import os
import sys
import logging
import json
from pymongo import MongoClient
from scrapy_nimbus.decorator import singleton, singleton_
from scrapy_nimbus.settings import NIMBUS_DEFAULT_NAME

__all__ = ["client", "ClientMongoDB", ]


@singleton_
class ClientMongoDB(object):
    connections = {}

    def init(self, name=None, **kwargs):
        if not name:
            return None
        if name in self.connections:
            return self.connections.get(name, None)
        _uri = kwargs.pop("uri", "")
        _db = kwargs.pop("db", NIMBUS_DEFAULT_NAME)
        if _uri:
            _client = MongoClient(_uri, **kwargs)
        else:
            _client = MongoClient(**kwargs)
        self.connections[name] = _client
        db = _client[_db] if _db else None
        return _client, db

    def get_cilent(self, name=NIMBUS_DEFAULT_NAME):
        return self.connections.get(name, None)

    def get_db(self, db=NIMBUS_DEFAULT_NAME, name=NIMBUS_DEFAULT_NAME):
        _client = self.get_cilent(name=name)
        if db and _client:
            return _client[db]
        return None


client = ClientMongoDB()
