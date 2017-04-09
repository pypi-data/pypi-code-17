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
from scrapy.http import Request
from scrapy.utils.misc import md5sum
from scrapy.utils.python import to_bytes
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem


class NimbusFilesPipeline(FilesPipeline):
    pass

