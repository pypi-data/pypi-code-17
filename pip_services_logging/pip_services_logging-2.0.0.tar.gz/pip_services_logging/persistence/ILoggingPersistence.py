# -*- coding: utf-8 -*-
"""
    pip_services_logging.persistence.ILoggingPersistence
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Logging persistence interface
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services_commons.run import ICleanable

class ILoggingPersistence(ICleanable):

    def get_page_by_filter(self, correlation_id, filter, paging):
        raise NotImplementedError('Method from interface definition')

    def create(self, correlation_id, message):
        raise NotImplementedError('Method from interface definition')
    
    def clear(self, correlation_id):
        raise NotImplementedError('Method from interface definition')
