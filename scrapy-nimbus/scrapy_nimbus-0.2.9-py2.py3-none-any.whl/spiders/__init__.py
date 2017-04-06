# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .base import BaseSpider
from .base import DataBaseSpider
from .base import MongoDBSpider
from .base import RedisSpider
from .base import DataBaseAndRedisSpider
from .base import MongoDBAndRedisSpider
from .base import DataBaseAndMongoDBAndRedisSpider

from .selenium import SeleniumSpider
from .phantomjs import PhantomJSSpider
