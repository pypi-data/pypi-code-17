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

__all__ = ["BaseXMLFeedSpider", "DBXMLFeedSpider", "MongoXMLFeedSpider", "RedisXMLFeedSpider",
           "DBAndRedisXMLFeedSpider", "MongoAndRedisXMLFeedSpider", "MongoAndDBXMLFeedSpider",
           "DBAndMongoAndRedisXMLFeedSpider", ]


class AbstractXMLFeedSpider(AbstractMixin, XMLFeedSpider):
    name = None
    allowed_domains = []
    start_urls = []

    def __init__(self, name=None, **kwargs):
        super(AbstractXMLFeedSpider, self).__init__(name, **kwargs)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(AbstractXMLFeedSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider.setup_nimbus(crawler.settings)
        return spider


class BaseXMLFeedSpider(BaseMixin, AbstractXMLFeedSpider):
    pass


class DBXMLFeedSpider(DBMixin, BaseXMLFeedSpider):
    pass


class MongoXMLFeedSpider(MongoMixin, BaseXMLFeedSpider):
    pass


class RedisXMLFeedSpider(RedisMixin, BaseXMLFeedSpider):
    pass


class DBAndRedisXMLFeedSpider(DBAndRedisMixin, BaseXMLFeedSpider):
    pass


class MongoAndRedisXMLFeedSpider(MongoAndRedisMixin, BaseXMLFeedSpider):
    pass


class MongoAndDBXMLFeedSpider(MongoAndDBMixin, BaseXMLFeedSpider):
    pass


class DBAndMongoAndRedisXMLFeedSpider(DBAndMongoAndRedisMixin, BaseXMLFeedSpider):
    pass
