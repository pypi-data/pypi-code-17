# -*- coding: utf-8 -*-
"""
    pip_clients_logging.log.HttpLogger
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Http logger implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .AbstractLogger import AbstractLogger
from ..version1.LoggingHttpClientV1 import LoggingHttpClientV1

class HttpLogger(AbstractLogger):

    def __init__(self):
        super(HttpLogger, self).__init__(LoggingHttpClientV1())
