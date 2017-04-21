# -*- coding: utf-8 -*-
"""
    pip_services_commons.config.OptionsResolver
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Options resolver implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ConfigParams import ConfigParams
from ..refer.Descriptor import Descriptor

class OptionsResolver(object):
    
    @staticmethod
    def resolve(config, config_as_default = False):
        options = config.get_section("options")

        if len(options) == 0 and config_as_default:
            options = config

        return options