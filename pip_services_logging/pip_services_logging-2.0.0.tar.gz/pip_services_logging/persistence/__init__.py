# -*- coding: utf-8 -*-
"""
    pip_services_logging.persistence.__init__
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Persistence module initialization
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

__all__ = [
    'ILoggingPersistence', 'LoggingMemoryPersistence'
]

from .ILoggingPersistence import ILoggingPersistence
from .LoggingMemoryPersistence import LoggingMemoryPersistence

