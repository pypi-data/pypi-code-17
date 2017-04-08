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
from scrapy import signals
from scrapy.settings import Settings
from scrapy.http import Request
from scrapy.utils.misc import md5sum
from scrapy.utils.python import to_bytes
from scrapy.exceptions import DropItem
from scrapy.exceptions import NotConfigured, IgnoreRequest
from scrapy_nimbus.settings import NIMBUS_DEFAULT_NAME
from scrapy_nimbus.spiders.mixin import AbstractMixin, BaseMixin


class NimbusDownloadMiddleware(object):
    def __init__(self, settings):
        super(NimbusDownloadMiddleware, self).__init__()

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider):
        func = getattr(spider, "post_setup_middleware", None)
        if callable(func):
            func()

    def process_request(self, request, spider):
        func = getattr(spider, "process_request", None)
        if callable(func):
            return func(request=request, spider=spider)

    def process_response(self, request, response, spider):
        func = getattr(spider, "process_response", None)
        if callable(func):
            return func(request=request, response=response, spider=spider)
        return response


