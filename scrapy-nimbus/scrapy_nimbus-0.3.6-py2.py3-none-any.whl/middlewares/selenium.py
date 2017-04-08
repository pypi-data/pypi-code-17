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
from scrapy.spiders import Rule, BaseSpider
from scrapy.http.request.form import FormRequest, Request
from scrapy.http.response.html import HtmlResponse
from scrapy.selector import Selector
from scrapy.utils.response import get_base_url
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC


class SeleniumDownloadMiddleware(object):
    driver = None

    def __init__(self, settings):
        self.driver = self.get_webdriver(system=platform.system())
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def get_webdriver(self, system="Linux"):
        raise NotImplementedError

    def spider_closed(self, spider):
        try:
            self.driver.quit()
        except Exception as e:
            spider.logger.error(e)
        finally:
            self.driver = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settins)
