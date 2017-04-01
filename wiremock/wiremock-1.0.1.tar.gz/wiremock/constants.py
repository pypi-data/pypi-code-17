from __future__ import unicode_literals
from calendar import timegm
from copy import deepcopy
import logging

from wiremock import __version__
from wiremock._compat import *


logger = logging.getLogger('wiremock')


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


DEFAULT_TIMEOUT = 30
DEFAULT_BASE_URL = 'http://localhost/__admin'
USER_AGENT = 'python_wiremock/%s'.format(__version__)
DEFAULT_HEADERS = {'Accept': 'application/json', 'Content-Type': 'application/json', 'user-agent': USER_AGENT}


@add_metaclass(Singleton)
class Config(object):
    timeout = DEFAULT_TIMEOUT
    base_url = DEFAULT_BASE_URL
    user_agent = USER_AGENT
    headers = DEFAULT_HEADERS

Config()  # pre-call once


def make_headers(**kwargs):
    headers = deepcopy(Config.headers)
    for key, value in kwargs.items():
        headers[key] = value
    return headers


def datetime_to_ms(dt):
    if isinstance(dt, integer_types):
        return dt
    else:
        tmp = timegm(date.utctimetuple())
        tmp += float(date.microsecond) / 1000000.0
        return long_(tmp * 1000.0)


__all__ = ['Config', 'make_headers', 'logger', 'datetime_to_ms']
