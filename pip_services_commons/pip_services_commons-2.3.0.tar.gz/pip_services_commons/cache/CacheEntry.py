# -*- coding: utf-8 -*-
"""
    pip_services_commons.cache.CacheEntry
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Cache entry implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import time

class CacheEntry(object):
    """
    Holds cached value for in-memory cache.
    """

    expiration = None
    key = None
    value = None

    def __init__(self, key, value, timeout):
        """
        Creates instance of the cache entry.
        
        Args:
            key: the unique key used to identify and locate the value.
            value: the cached value.
            timeout: time to live for the object in milliseconds
        """
        self.key = key
        self.value = value
        self.expiration = time.clock() * 1000 + timeout

    def set_value(self, value, timeout):
        """
        Changes the cached value and updates creation time.
        
        Args:
            value: the new cached value.
            timeout: time to live for the object in milliseconds

        Returns: None
        """
        self.value = value
        self.expiration = time.clock() * 1000 + timeout

    def is_expired(self):
        """
        Checks if the object expired

        Returns: True if object expired
        """
        return self.expiration < time.clock() * 1000
