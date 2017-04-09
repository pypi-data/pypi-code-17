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

from .selenium import SeleniumDownloadMiddleware


class PhantomJSDownloadMiddleware(SeleniumDownloadMiddleware):
    page_source_encoding = "utf-8"

    def get_webdriver(self, system="Linux"):
        if system.find("Linux") >= 0:
            driver = webdriver.PhantomJS()
        elif system.find("Darwin") >= 0:
            driver = webdriver.PhantomJS()
        elif system.find("Windows") >= 0:
            driver = webdriver.PhantomJS()
        else:
            driver = webdriver.PhantomJS()
        driver.set_page_load_timeout(10)
        return driver

    def process_request(self, request, spider):
        if request.meta.has_key('PhantomJS'):
            self.driver.get(request.url)
            content = self.driver.page_source.encode(self.page_source_encoding)
            return HtmlResponse(request.url, encoding=self.page_source_encoding, body=content, request=request)
