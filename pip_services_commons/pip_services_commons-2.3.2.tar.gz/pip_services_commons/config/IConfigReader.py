# -*- coding: utf-8 -*-
"""
    pip_services_commons.config.IConfigReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    interface for configuration readers
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IConfigReader:

    def read_config(correlation_id, parameters):
        raise NotImplementedError('Method from interface definition')
