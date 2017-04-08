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
from scrapy_nimbus.data import dbclient
from scrapy_nimbus.spiders.mixin import AbstractMixin, BaseMixin


class NimbusPipeline(object):
    def __init__(self):
        super(NimbusPipeline, self).__init__()

    def process_item(self, item, spider, **kwargs):
        func = getattr(spider, "process_item", None)
        if callable(func):
            item = func(item=item, spider=spider, **kwargs)
        return item

    def open_spider(self, spider):
        func = getattr(spider, "post_setup_pipeline", None)
        if callable(func):
            func()

    def close_spider(self, spider):
        func = getattr(spider, "close_nimbus", None)
        if callable(func):
            func()
