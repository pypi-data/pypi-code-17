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
from scrapy.spiders import Rule
from scrapy.http.request.form import FormRequest, Request
from scrapy.http.response.html import HtmlResponse
from scrapy.selector import Selector
from scrapy.utils.response import get_base_url
from scrapy_nimbus.settings import DEFAULT_DATABASE, DEFAULT_MONGODB, DEFAULT_REDIS
from scrapy_nimbus.data import dbclient
from scrapy_nimbus.data import mongodbclient
from scrapy_nimbus.data import redisclient
from .mixin import *


__all__ = ["BaseSpider", "DataBaseSpider", "MongoSpider", "RedisSpider", "DataBaseAndRedisSpider",
           "MongoAndRedisSpider", "MongoAndDataBaseSpider", "DataBaseAndMongoAndRedisSpider", ]


class AbstractSpider(AbstractMixin, Spider):
    name = None
    allowed_domains = []
    start_urls = []

    def __init__(self, name=None, **kwargs):
        super(AbstractSpider, self).__init__(name, **kwargs)

    def start_requests(self):
        return super(AbstractSpider, self).start_requests()

    def parse(self, response):
        raise NotImplementedError

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(AbstractSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider.setup_nimbus(crawler.settings)
        return spider


class BaseSpider(BaseMixin, AbstractSpider):
    pass


class DataBaseSpider(DataBaseMixin, BaseSpider):
    @staticmethod
    def close(spider, reason):
        result = super(DataBaseSpider, spider).close(spider, reason)
        closed = getattr(spider, 'close_nimbus', None)
        if callable(closed):
            spider.close_nimbus()
        return result


class MongoSpider(MongoMixin, BaseSpider):
    @staticmethod
    def close(spider, reason):
        result = super(MongoSpider, spider).close(spider, reason)
        closed = getattr(spider, 'close_nimbus', None)
        if callable(closed):
            spider.close_nimbus()
        return result


class RedisSpider(RedisMixin, BaseSpider):
    @staticmethod
    def close(spider, reason):
        result = super(RedisSpider, spider).close(spider, reason)
        closed = getattr(spider, 'close_nimbus', None)
        if callable(closed):
            spider.close_nimbus()
        return result


class DataBaseAndRedisSpider(DataBaseAndRedisMixin, BaseSpider):
    @staticmethod
    def close(spider, reason):
        result = super(DataBaseAndRedisSpider, spider).close(spider, reason)
        closed = getattr(spider, 'close_nimbus', None)
        if callable(closed):
            spider.close_nimbus()
        return result


class MongoAndRedisSpider(MongoAndRedisMixin, BaseSpider):
    @staticmethod
    def close(spider, reason):
        result = super(MongoAndRedisSpider, spider).close(spider, reason)
        closed = getattr(spider, 'close_nimbus', None)
        if callable(closed):
            spider.close_nimbus()
        return result


class MongoAndDataBaseSpider(MongoAndDataBaseMixin, BaseSpider):
    @staticmethod
    def close(spider, reason):
        result = super(MongoAndDataBaseSpider, spider).close(spider, reason)
        closed = getattr(spider, 'close_nimbus', None)
        if callable(closed):
            spider.close_nimbus()
        return result


class DataBaseAndMongoAndRedisSpider(DataBaseAndMongoAndRedisMixin, BaseSpider):
    @staticmethod
    def close(spider, reason):
        result = super(DataBaseAndMongoAndRedisSpider, spider).close(spider, reason)
        closed = getattr(spider, 'close_nimbus', None)
        if callable(closed):
            spider.close_nimbus()
        return result
