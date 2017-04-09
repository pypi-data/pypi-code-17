# -*- coding: utf-8 -*-
"""
    pip_clients_logging.log.DirectLogger
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Direct logger implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .AbstractLogger import AbstractLogger
from ..version1.LoggingDirectClientV1 import LoggingDirectClientV1

class DirectLogger(AbstractLogger):

    def __init__(self):
        super(DirectLogger, self).__init__(LoggingDirectClientV1())
