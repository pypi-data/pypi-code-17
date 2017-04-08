# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .base import BaseSpider
from .base import DataBaseSpider
from .base import MongoSpider
from .base import RedisSpider
from .base import DataBaseAndRedisSpider
from .base import MongoAndRedisSpider
from .base import MongoAndDataBaseSpider
from .base import DataBaseAndMongoAndRedisSpider

from .selenium import SeleniumSpider
from .phantomjs import PhantomJSSpider
