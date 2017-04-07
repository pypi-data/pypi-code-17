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
from scrapy_nimbus.data import redisclient


class RedisAbstractPipeline(object):
    pass


class RedisMixinPipeline(RedisAbstractPipeline):
    pass
