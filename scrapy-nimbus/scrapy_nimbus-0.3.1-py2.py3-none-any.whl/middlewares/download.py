# -*- coding: utf-8 -*-
from __future__ import absolute_import

"""
Package Description
"""
import os
import sys
import logging
import json

from scrapy import signals
from scrapy.exceptions import NotConfigured, IgnoreRequest
from scrapy.exceptions import DropItem


class DuplicationUrlDownloadMiddleware(object):
    def __init__(self, settings):
        super(DuplicationUrlDownloadMiddleware, self).__init__()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        if not self.status:
            return
        url = request.url
        if url in self.links:
            spider.logger.debug(u"IGNORE URL:{}".format(url))
            raise IgnoreRequest()