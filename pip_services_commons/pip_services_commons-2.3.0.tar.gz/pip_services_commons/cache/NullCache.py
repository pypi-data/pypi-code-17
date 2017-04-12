# -*- coding: utf-8 -*-
"""
    pip_services_commons.cache.NullCache
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Null cache component implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ICache import ICache

class NullCache(object, ICache):
    """
    Null cache component that doesn't do caching at all.
    It's mainly used in testing. However, it can be temporary
    used to disable cache to troubleshoot problems or study
    effect of caching on overall system performance. 
    """

    def retrieve(self, correlation_id, key):
        return None

    def store(self, correlation_id, key, value, timeout):
        return value
    
    def remove(self, correlation_id, key):
        pass
