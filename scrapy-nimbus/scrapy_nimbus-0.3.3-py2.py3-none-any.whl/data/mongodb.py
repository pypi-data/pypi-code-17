# -*- coding: utf-8 -*-
from __future__ import absolute_import

"""
Package Description
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
        if _uri:
            _client = MongoClient(_uri, **kwargs)
        else:
            _client = MongoClient(**kwargs)
        self.connections[name] = _client
        return _client

    def get_cilent(self, name=NIMBUS_DEFAULT_NAME):
        return self.connections.get(name, None)


client = ClientMongoDB()
