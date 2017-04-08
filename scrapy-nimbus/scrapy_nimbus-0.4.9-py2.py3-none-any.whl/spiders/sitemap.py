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

__all__ = ["BaseSitemapSpider", "DBSitemapSpider", "MongoSitemapSpider", "RedisSitemapSpider",
           "DBAndRedisSitemapSpider", "MongoAndRedisSitemapSpider", "MongoAndDBSitemapSpider",
           "DBAndMongoAndRedisSitemapSpider", ]


class AbstractSitemapSpider(AbstractMixin, SitemapSpider):
    name = None
    allowed_domains = []
    start_urls = []

    def __init__(self, name=None, **kwargs):
        super(AbstractSitemapSpider, self).__init__(name, **kwargs)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(AbstractSitemapSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider.setup_nimbus(crawler.settings)
        return spider


class BaseSitemapSpider(BaseMixin, AbstractSitemapSpider):
    pass


class DBSitemapSpider(DBMixin, BaseSitemapSpider):
    pass


class MongoSitemapSpider(MongoMixin, BaseSitemapSpider):
    pass


class RedisSitemapSpider(RedisMixin, BaseSitemapSpider):
    pass


class DBAndRedisSitemapSpider(DBAndRedisMixin, BaseSitemapSpider):
    pass


class MongoAndRedisSitemapSpider(MongoAndRedisMixin, BaseSitemapSpider):
    pass


class MongoAndDBSitemapSpider(MongoAndDBMixin, BaseSitemapSpider):
    pass


class DBAndMongoAndRedisSitemapSpider(DBAndMongoAndRedisMixin, BaseSitemapSpider):
    pass
