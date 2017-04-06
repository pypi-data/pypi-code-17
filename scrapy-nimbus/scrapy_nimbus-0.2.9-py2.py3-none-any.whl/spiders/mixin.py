# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import sys
import json
import datetime
import time
import urlparse
import random
import platform
import scrapy
from pydispatch import dispatcher
from scrapy import signals
from scrapy.spiders import Spider, CrawlSpider, CSVFeedSpider, SitemapSpider, XMLFeedSpider
from scrapy.spiders import Rule, BaseSpider
from scrapy.http.request.form import FormRequest, Request
from scrapy.http.response.html import HtmlResponse
from scrapy.selector import Selector
from scrapy.utils.response import get_base_url
from scrapy_nimbus.settings import DEFAULT_DATABASE_SQLITE, DEFAULT_DATABASE, DEFAULT_MONGODB, DEFAULT_REDIS
from scrapy_nimbus.settings import NIMBUS_SETTING_CLIENT_DB, NIMBUS_SETTING_CLIENT_MONGODB, NIMBUS_SETTING_CLIENT_REDIS
from scrapy_nimbus.settings import NIMBUS_DEFAULT_NAME
from scrapy_nimbus.data import dbclient
from scrapy_nimbus.data import mongodbclient
from scrapy_nimbus.data import redisclient

__all__ = ["BaseMixin", "DataBaseMixin", "MongoDBMixin", "RedisMixin", "DataBaseAndRedisMixin",
           "MongoDBAndRedisMixin", "DataBaseAndMongoDBAndRedisMixin", "AbstractMixin", ]


class AbstractMixin(object):
    def setup_nimbus(self, settings):
        raise NotImplementedError

    def close_nimbus(self):
        raise NotImplementedError

    def process_item(self, item, spider, **kwargs):
        raise NotImplementedError


class BaseMixin(AbstractMixin):

    def setup_nimbus(self, settings):
        pass

    def close_nimbus(self):
        pass


class DataBaseMixin(BaseMixin):
    nimbus_db_name = NIMBUS_DEFAULT_NAME
    nimbus_db_engine = None
    nimbus_db_session = None
    auto_create_table = False

    def setup_nimbus(self, settings):
        self._init_client_db()

    def close_nimbus(self):
        self._close_client_db()

    def get_db_session(self):
        return self.nimbus_db_session

    def get_db_engine(self):
        return self.nimbus_db_engine

    def create_table(self):
        raise NotImplementedError

    def create_model(self, item, *args, **kwargs):
        raise NotImplementedError

    def _init_client_db(self):
        self.logger.debug(u"init client db")
        name = self.nimbus_db_name
        configs = self.settings.get(NIMBUS_SETTING_CLIENT_DB, {})
        if name and isinstance(configs, (dict,)) and name in configs:
            config = configs.get(name, DEFAULT_DATABASE_SQLITE)
            self.logger.debug(u"{name}:{config}".format(name=name, config=config))
            dbclient.init(name, **config)
            self.nimbus_db_engine = dbclient.get_engine(name=name)
            self.nimbus_db_session = dbclient.get_session(name=name)
        else:
            self.logger.warning(u"EMPTY {name}:{configs}".format(name=name, configs=configs))
            self.nimbus_db_engine = None
            self.nimbus_db_session = None

    def _close_client_db(self):
        pass


class MongoDBMixin(BaseMixin):
    nimbus_mongodb_name = NIMBUS_DEFAULT_NAME
    nimbus_mongodb = None

    def setup_nimbus(self, settings):
        self._init_client_mongodb()

    def close_nimbus(self):
        self._close_client_mongodb()

    def _init_client_mongodb(self):
        self.logger.debug(u"init client mongodb")
        name = self.nimbus_mongodb_name
        configs = self.settings.get(NIMBUS_SETTING_CLIENT_MONGODB, {})
        if name and isinstance(configs, (dict,)) and name in configs:
            config = configs.get(name, DEFAULT_MONGODB)
            self.logger.debug(u"{name}:{config}".format(name=name, config=config))
            self.nimbus_mongodb = mongodbclient.init(name, **config)
        else:
            self.logger.warning(u"EMPTY {name}:{configs}".format(name=name, configs=configs))
            self.nimbus_mongodb = None

    def _close_client_mongodb(self):
        pass


class RedisMixin(BaseMixin):
    nimbus_redis_name = NIMBUS_DEFAULT_NAME
    nimbus_redis = None

    def setup_nimbus(self, settings):
        self._init_client_redis()

    def close_nimbus(self):
        self._close_client_redis()

    def _init_client_redis(self):
        self.logger.debug(u"init client redis")
        name = self.nimbus_redis_name
        configs = self.settings.get(NIMBUS_SETTING_CLIENT_REDIS, {})
        if name and isinstance(configs, (dict,)) and name in configs:
            config = configs.get(name, DEFAULT_REDIS)
            self.logger.debug(u"{name}:{config}".format(name=name, config=config))
            self.nimbus_redis = redisclient.init(name, **config)
        else:
            self.logger.warning(u"EMPTY {name}:{configs}".format(name=name, configs=configs))
            self.nimbus_redis = None

    def _close_client_redis(self):
        pass


class DataBaseAndRedisMixin(DataBaseMixin, RedisMixin):
    def setup_nimbus(self, settings):
        self._init_client_db()
        self._init_client_redis()

    def close_nimbus(self):
        self._close_client_db()
        self._close_client_redis()


class MongoDBAndRedisMixin(MongoDBMixin, RedisMixin):
    def setup_nimbus(self, settings):
        self._init_client_mongodb()
        self._init_client_redis()

    def close_nimbus(self):
        self._close_client_mongodb()
        self._close_client_redis()


class DataBaseAndMongoDBAndRedisMixin(DataBaseMixin, MongoDBMixin, RedisMixin):
    def setup_nimbus(self, settings):
        self._init_client_db()
        self._init_client_mongodb()
        self._init_client_redis()

    def close_nimbus(self):
        self._close_client_db()
        self._close_client_mongodb()
        self._close_client_redis()


