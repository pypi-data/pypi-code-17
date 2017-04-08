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


__all__ = ["BaseSpider", "DBSpider", "MongoSpider", "RedisSpider", "DBAndRedisSpider",
           "MongoAndRedisSpider", "MongoAndDBSpider", "DBAndMongoAndRedisSpider", ]


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


class DBSpider(DBMixin, BaseSpider):
    pass


class MongoSpider(MongoMixin, BaseSpider):
    pass


class RedisSpider(RedisMixin, BaseSpider):
    pass


class DBAndRedisSpider(DBAndRedisMixin, BaseSpider):
    pass


class MongoAndRedisSpider(MongoAndRedisMixin, BaseSpider):
    pass


class MongoAndDBSpider(MongoAndDBMixin, BaseSpider):
    pass


class DBAndMongoAndRedisSpider(DBAndMongoAndRedisMixin, BaseSpider):
    pass
