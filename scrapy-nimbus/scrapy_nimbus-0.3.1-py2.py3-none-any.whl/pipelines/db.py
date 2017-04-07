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
from scrapy_nimbus.spiders.mixin import DataBaseMixin


class DataBaseAbstractPipeline(object):

    def __init__(self):
        super(DataBaseAbstractPipeline, self).__init__()
        self._db_session = None

    def open_spider(self, spider):
        self._db_session = self.get_db_session(spider)
        self.create_db_table(spider)

    def process_item(self, item, spider):
        if not self._db_session:
            return
        item = self.process_db_item(item=item, spider=spider, db_session=self._db_session)
        return item

    def close_spider(self, spider):
        if not self._db_session:
            return
        try:
            self._db_session.commit()
        except Exception as e:
            self._db_session.rollback()
            spider.logger.error(e)
        # except Exception as e:
        #     spider.logger.error(e)
        finally:
            self._db_session.close()

    def get_db_session(self, spider, *args, **kwargs):
        raise NotImplementedError

    def create_db_table(self, spider, *args, **kwargs):
        raise NotImplementedError

    def process_db_item(self, item, spider, db_session, *args, **kwargs):
        raise NotImplementedError


class DataBaseMixinPipeline(DataBaseAbstractPipeline):
    def create_db_table(self, spider, *args, **kwargs):
        if not isinstance(spider, DataBaseMixin):
            return
        return spider.create_table()

    def get_db_session(self, spider, *args, **kwargs):
        if not isinstance(spider, DataBaseMixin):
            return
        return spider.get_db_session()

    def process_db_item(self, item, spider, db_session, *args, **kwargs):
        try:
            if not db_session or not isinstance(spider, DataBaseMixin):
                return
            model = spider.create_model(item)
            if not model:
                return
            db_session.add(model)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            spider.logger.error(e)
        # except Exception as e:
        #     spider.logger.error(e)
        return item

