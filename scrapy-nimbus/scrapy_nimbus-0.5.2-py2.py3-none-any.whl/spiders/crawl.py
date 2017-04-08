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

__all__ = ["BaseCrawlSpider", "DBCrawlSpider", "MongoCrawlSpider", "RedisCrawlSpider",
           "DBAndRedisCrawlSpider", "MongoAndRedisCrawlSpider", "MongoAndDBCrawlSpider",
           "DBAndMongoAndRedisCrawlSpider", ]


class AbstractCrawlSpider(AbstractMixin, CrawlSpider):
    name = None
    allowed_domains = []
    start_urls = []

    def __init__(self, name=None, **kwargs):
        super(AbstractCrawlSpider, self).__init__(name, **kwargs)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(AbstractCrawlSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider.setup_nimbus(crawler.settings)
        return spider


class BaseCrawlSpider(BaseMixin, AbstractCrawlSpider):
    pass


class DBCrawlSpider(DBMixin, BaseCrawlSpider):
    pass


class MongoCrawlSpider(MongoMixin, BaseCrawlSpider):
    pass


class RedisCrawlSpider(RedisMixin, BaseCrawlSpider):
    pass


class DBAndRedisCrawlSpider(DBAndRedisMixin, BaseCrawlSpider):
    pass


class MongoAndRedisCrawlSpider(MongoAndRedisMixin, BaseCrawlSpider):
    pass


class MongoAndDBCrawlSpider(MongoAndDBMixin, BaseCrawlSpider):
    pass


class DBAndMongoAndRedisCrawlSpider(DBAndMongoAndRedisMixin, BaseCrawlSpider):
    pass
