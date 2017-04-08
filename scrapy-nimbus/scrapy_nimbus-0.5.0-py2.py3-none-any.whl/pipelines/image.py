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
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


class NimbusImagesPipeline(ImagesPipeline):
    pass


class NimbusExtendImagesPipeline(ImagesPipeline):
    NIMBUS_IMAGE_META_NAME = 'meta_name'
    NIMBUS_IMAGE_KEY_URL = "url"
    NIMBUS_IMAGE_KEY_NAME = "name"

    def __init__(self, store_uri, download_func=None, settings=None):
        super(NimbusExtendImagesPipeline, self).__init__(store_uri, download_func, settings)

    def get_media_requests(self, item, info):
        for x in item.get(self.images_urls_field, []):
            if isinstance(x, six.string_types):
                yield Request(url=x)
            elif isinstance(x, dict) and x.get(self.NIMBUS_IMAGE_KEY_URL, None) \
                    and x.get(self.NIMBUS_IMAGE_KEY_NAME, None):
                yield Request(x.get(self.NIMBUS_IMAGE_KEY_URL),
                              meta={self.NIMBUS_IMAGE_META_NAME: x.get(self.NIMBUS_IMAGE_KEY_NAME, "")})
            else:
                continue

    def item_completed(self, results, item, info):
        return super(NimbusExtendImagesPipeline, self).item_completed(results, item, info)

    def file_path(self, request, response=None, info=None):
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('NimbusExtendImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
                          'please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url
        name = request.meta.get(self.NIMBUS_IMAGE_META_NAME, "")
        if name:
            image_guid = name
        else:
            image_guid = hashlib.md5(to_bytes(url)).hexdigest()  # change to request.url after deprecation
        return 'full/%s.jpg' % (image_guid,)

    def thumb_path(self, request, thumb_id, response=None, info=None):
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('NimbusExtendImagesPipeline.thumb_key(url) method is deprecated, please use '
                          'thumb_path(request, thumb_id, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url
        name = response.meta.get(self.NIMBUS_IMAGE_META_NAME, "")
        if name:
            thumb_guid = name
        else:
            thumb_guid = hashlib.md5(to_bytes(url)).hexdigest()  # change to request.url after deprecation
        return 'thumbs/%s/%s.jpg' % (thumb_id, thumb_guid)
