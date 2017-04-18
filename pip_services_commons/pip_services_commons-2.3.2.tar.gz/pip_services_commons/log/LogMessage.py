# -*- coding: utf-8 -*-
"""
    pip_services_commons.logs.LogMessage
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Log message implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import datetime

class LogMessage(object):
    time = None
    source = None
    level = None
    correlation_id = None
    error = None
    message = None

    def __init__(self, level = None, source = None, correlation_id = None, error = None, message = None):
        self.time = datetime.datetime.utcnow()
        self.level = level
        self.source = source
        self.correlation_id = correlation_id
        self.error = error
        self.message = message
