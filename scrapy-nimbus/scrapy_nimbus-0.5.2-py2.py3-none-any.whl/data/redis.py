# -*- coding: utf-8 -*-
from __future__ import absolute_import
"""
Package Description
"""
import os
import sys
import logging
import json
import redis
from scrapy_nimbus.decorator import singleton, singleton_
from scrapy_nimbus.settings import NIMBUS_DEFAULT_NAME

__all__ = ["client", "ClientRedis", ]


@singleton_
class ClientRedis(object):
    connections = {}

    def init(self, name=None, **kwargs):
        if not name:
            return None
        if name in self.connections:
            return self.connections.get(name, None)
        engine = redis.StrictRedis(**kwargs)
        self.connections[name] = engine
        return engine

    def get_connection(self, name=NIMBUS_DEFAULT_NAME):
        return self.connections.get(name, None)


client = ClientRedis()
