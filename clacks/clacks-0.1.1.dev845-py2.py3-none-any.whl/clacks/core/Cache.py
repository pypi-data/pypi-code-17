#!/usr/bin/env python3

"""Simple file based caching mechanism."""

import os.path
import pickle
import time

from .env import resolvePath

_cachepath = 'caches/GtCache'


def get_file(name):
    """Resolve given cache entry to disk location"""
    return resolvePath(_cachepath, name+'.pickle')


def set(name, value):  # pylint: disable=redefined-builtin
    """Set given cache line to given value

    @param name string cache line name. It should follow file naming conventions.
    @param value object - any serializable variable

    @return its second argument

    """
    with get_file(name).open('wb') as f:
        pickle.dump(value, f)
    return value


def get(name, expires=None, callback=None, failover=False):
    """
    fetches cached value from disk

    @param name string - cache line identifier to fetch. It should follow file
        naming conventions.
    @param expires int - if given and cache line is older than given time in seconds
       and no callback is provided throws KeyError. If 0 then callback is always used.
    @param callback function - callback function used if cache is invalid or doesn't
        exist; its result is stored as new cache value and returned;
        function may be in any form that call_user_func() accepts.
    @param failover bool (optional, False by default), if set and callback function
        raises exception, it is ignored and cached value is returned instead
        (despite it is outdated) unless it doesn't exist then regular
        KeyError is thrown.
    @return restored variable contents
    """

    validated = (expires != 0) and isValid(name, expires)
    if (expires is not None) and not validated and callback is None:
        raise KeyError(name)

    if validated:
        try:
            with get_file(name).open('rb') as f:
                return pickle.load(f)
        except Exception:  # pylint: disable=broad-except
            pass

    elif callback is None:
        raise KeyError(name)

    else:
        try:
            return set(name, callback())
        except Exception:  # pylint:  disable=broad-except
            if not failover:
                raise
        return get(name)


def delete(name):
    """ removes given cache line from disk

    @param id string cache line name
    @return void
    """

    if get_file(name).exists():
        os.unlink(str(get_file(name)))


def isValid(name, expires=None):
    """ validates if cache line is not older than given time in seconds

    @param id string cache line name.
    @param expires int cache line age limit in seconds,
        checks for cache existence if not provided
    @return True if cache is still valid, False otherwise
    """
    fpath = get_file(name)
    if expires is None:
        return fpath.exists()

    if not fpath.exists():
        return False

    return (time.time()-fpath.stat().st_mtime) <= expires
