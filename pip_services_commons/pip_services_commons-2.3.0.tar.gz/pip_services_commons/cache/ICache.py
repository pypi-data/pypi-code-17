# -*- coding: utf-8 -*-
"""
    pip_services_commons.cache.ICache
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for caching components.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class ICache:
    """
    Transient cache which is used to bypass persistence to increase overall system performance.
    """

    def retrieve(self, correlation_id, key):
        """
        Retrieves a value from the cache by unique key.
        It is recommended to use either string GUIDs like '123456789abc'
        or unique natural keys prefixed with the functional group
        like 'pip-services-storage:block-123'.

        Args:
            correlation_id: a unique transaction id to trace calls across components
            key: a unique key to locate value in the cache.

        Returns: a cached value or None if value wasn't found or timeout expired.
        """
        raise NotImplementedError('Method from interface definition')

    def store(self, correlation_id, key, value, timeout):
        """
        Stores value identified by unique key in the cache.
        Stale timeout is configured in the component options.

        Args:
            correlation_id: a unique transaction id to trace calls across components
            key: a unique key to locate value in the cache.
            value: a value to store.
            timeout: time for value to live in milliseconds

        Returns: a cached value stored in the cache.
        """
        raise NotImplementedError('Method from interface definition')

    def remove(self, correlation_id, key):
        """
        Removes value stored in the cache.

        Args:
            correlation_id: a unique transaction id to trace calls across components
            key: a unique key to locate value in the cache.
        """
        raise NotImplementedError('Method from interface definition')
