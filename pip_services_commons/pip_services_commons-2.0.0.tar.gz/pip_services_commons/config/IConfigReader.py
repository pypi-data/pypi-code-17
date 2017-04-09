# -*- coding: utf-8 -*-
"""
    pip_services_commons.config.IConfigReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    interface for configuration readers
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ConfigParams import ConfigParams

class IConfigReader:

    def read_config(correlation_id):
        raise NotImplementedError('Method from interface definition')
        
    def read_config_section(correlation_id, section):
        raise NotImplementedError('Method from interface definition')
