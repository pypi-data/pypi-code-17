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

from .base import BaseSpider


class SeleniumSpider(BaseSpider):
    name = "selenium_spider"
    allowed_domains = []
    start_urls = []
    driver = None

    def __init__(self, name=None, **kwargs):
        super(SeleniumSpider, self).__init__(name, **kwargs)
        self.driver = self.init_webdriver(system=platform.system())
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        try:
            self.driver.quit()
        except Exception as e:
            self.logger.error(e)
        finally:
            self.driver = None

    def init_webdriver(self, system="Linux"):
        raise NotImplementedError

    def parse(self, response):
        raise NotImplementedError

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def test(self, response):
        print response, response.url
        self.driver.get(response.url)
        try:
            element = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'table')))
            print 'element:\n', element
        except Exception, e:
            print "wait failed"
