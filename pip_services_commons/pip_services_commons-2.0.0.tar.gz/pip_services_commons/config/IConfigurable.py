# -*- coding: utf-8 -*-
"""
    pip_services_commons.config.IConfigurable
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for components that require configuration
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IConfigurable:
    """
     Interface for components that require configuration
    """

    def configure(self, config):
        """
        Sets component configuration

        Args:
            config: configuration parameters

        Raise: ConfigException when configuration is wrong
        """
        raise NotImplementedError('Method from interface definition')
