"""Memcached support tools 

Copyright 2010-2012 Etienne Robillard <erob@gthcfoundation.org>
All rights reserved.

<LICENSE=ISC>
"""

import memcache
import functools
import logging

log = logging.getLogger(__name__)

__all__ = ['MemcacheStore', 'store', 'cached']

class MemcacheStore(memcache.Client):
    """Simple wrapper over ``memcache.Client`` to encapsulate Django
    settings logic.

    Obtain a default ``memcache.Client`` object by looking up memcached
    server settings with the provided ``settings`` module argument ::

    .. coding: Python

        >>> from notmm.utils.django_settings import LazySettings
        >>> mc = MemcacheStore(settings=LazySettings())
        >>> repr(mc)
        <MemcacheStore: 'xxx'>
    """
    CACHE_BACKEND_LOCATION = '127.0.0.1:11211'
    
    def __init__(self, key_value='default', debug=2):
        self.netloc = self.CACHE_BACKEND_LOCATION
        super(MemcacheStore, self).__init__([self.netloc,], debug=debug)
    
    def __repr__(self):
        return "<MemcacheStore: %s>" % self.netloc


store = MemcacheStore()

def cached(time=1200):
  def decorator(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
      key = '%s' % function.__name__
      value = store.get(key)
      log.debug('Cache lookup for %s, found? %s', key, value != None)
      if not value:
        value = function(*args, **kwargs)
        store.set(key, value, time=time)
      return value
    return wrapper
  return decorator
