# -*- coding: utf-8 -*-
from __future__ import absolute_import

"""
Package Description
"""
import os
import sys
import logging
import json
import codecs
import functools
import hashlib
import six
import scrapy
from scrapy.settings import Settings
from scrapy.http import Request
from scrapy.utils.misc import md5sum
from scrapy.utils.python import to_bytes
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy_nimbus.settings import NIMBUS_DEFAULT_NAME
from scrapy_nimbus.data import mongodbclient
from scrapy_nimbus.spiders.mixin import MongoDBMixin


class MongoDBAbstractPipeline(object):
    db_name = None

    def __init__(self, *args, **kwargs):
        super(MongoDBAbstractPipeline, self).__init__()
        self.client = None
        self.db = None
        self.collection = None

    def open_spider(self, spider):
        self.client = self.get_client(spider=spider)
        self.db = self.get_db(spider=spider, client=self.client)

    def process_item(self, item, spider):
        self.collection = self.get_collection(item=item, spider=spider, client=self.client, db=self.db)
        if self.collection:
            item = self.process_db_item(item=item, spider=spider, collection=self.collection)
        return item

    def close_spider(self, spider):
        if not self.client:
            return
        self.collection = None
        self.db = None
        self.client.close()
        self.client = None

    def get_client(self, spider, *args, **kwargs):
        raise NotImplementedError

    def get_db(self, spider, client, *args, **kwargs):
        raise NotImplementedError

    def get_collection(self, item, spider, client, db, *args, **kwargs):
        raise NotImplementedError

    def process_db_item(self, item, spider, client, *args, **kwargs):
        raise NotImplementedError


class MongoDBMixinPipeline(MongoDBAbstractPipeline):
    def __init__(self, *args, **kwargs):
        super(MongoDBPipeline, self).__init__(*args, **kwargs)

    def get_client(self, spider, *args, **kwargs):
        if isinstance(spider, MongoDBMixin):
            _name = spider.nimbus_mongodb_name
        else:
            _name = spider.name
        return mongodbclient.get_cilent(name=_name)

    def get_db(self, spider, client, *args, **kwargs):
        if client:
            return client[self.db_name]
        else:
            return None

    def get_collection(self, item, spider, client, db, *args, **kwargs):
        collection_name = item.__class__.__name__
        if db and collection_name:
            return db[collection_name]
        else:
            return None

    def process_db_item(self, item, spider, collection, *args, **kwargs):
        if collection:
            collection.insert(dict(item))
        return item
