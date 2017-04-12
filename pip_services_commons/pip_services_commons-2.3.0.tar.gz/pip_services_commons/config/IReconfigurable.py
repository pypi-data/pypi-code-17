# -*- coding: utf-8 -*-
"""
    pip_services_commons.config.IReconfigurable
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for components that can be reconfigured when configuration changes
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IConfigurable import IConfigurable

class IReconfigurable(IConfigurable):
    """
    Interface for components that can be reconfigured when configuration changes
    """
    pass