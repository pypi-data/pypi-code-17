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

__all__ = ["BaseCSVFeedSpider", "DataBaseCSVFeedSpider", "MongoCSVFeedSpider", "RedisCSVFeedSpider",
           "DataBaseAndRedisCSVFeedSpider", "MongoAndRedisCSVFeedSpider", "MongoAndDataBaseCSVFeedSpider",
           "DataBaseAndMongoAndRedisCSVFeedSpider", ]


class AbstractCSVFeedSpider(AbstractMixin, CSVFeedSpider):
    name = None
    allowed_domains = []
    start_urls = []

    def __init__(self, name=None, **kwargs):
        super(AbstractCSVFeedSpider, self).__init__(name, **kwargs)

    def start_requests(self):
        return super(AbstractCSVFeedSpider, self).start_requests()

    def parse(self, response):
        raise NotImplementedError

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(AbstractCSVFeedSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider.setup_nimbus(crawler.settings)
        return spider


class BaseCSVFeedSpider(BaseMixin, AbstractCSVFeedSpider):
    pass


class DataBaseCSVFeedSpider(DataBaseMixin, BaseCSVFeedSpider):
    pass


class MongoCSVFeedSpider(MongoMixin, BaseCSVFeedSpider):
    pass


class RedisCSVFeedSpider(RedisMixin, BaseCSVFeedSpider):
    pass


class DataBaseAndRedisCSVFeedSpider(DataBaseAndRedisMixin, BaseCSVFeedSpider):
    pass


class MongoAndRedisCSVFeedSpider(MongoAndRedisMixin, BaseCSVFeedSpider):
    pass


class MongoAndDataBaseCSVFeedSpider(MongoAndDataBaseMixin, BaseCSVFeedSpider):
    pass


class DataBaseAndMongoAndRedisCSVFeedSpider(DataBaseAndMongoAndRedisMixin, BaseCSVFeedSpider):
    pass
