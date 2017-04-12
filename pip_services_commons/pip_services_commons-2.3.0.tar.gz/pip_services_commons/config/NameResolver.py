# -*- coding: utf-8 -*-
"""
    pip_services_commons.config.NameResolver
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Name resolver implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ConfigParams import ConfigParams
from ..refer.Descriptor import Descriptor

class NameResolver(object):
    
    @staticmethod
    def resolve(config, default_name = None):
        name = config.get_as_nullable_string("name")
        name = name if name != None else config.get_as_nullable_string("id")

        if name == None:
            descriptor_str = config.get_as_nullable_string("descriptor")
            descriptor = Descriptor.from_string(descriptor_str)
            if descriptor != None:
                name = descriptor.get_name()

        return name if name != None else default_name
