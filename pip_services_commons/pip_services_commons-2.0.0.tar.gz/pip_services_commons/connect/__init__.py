# -*- coding: utf-8 -*-
"""
    pip_services_commons.connect.__init__
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Connection module initialization
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

__all__ = [ 'ConnectionParams', 'IDiscovery', 'ConnectionResolver',
    'MemoryDiscovery', 'DefaultDiscoveryFactory' ]

from .ConnectionParams import ConnectionParams
from .IDiscovery import IDiscovery
from .ConnectionResolver import ConnectionResolver
from .MemoryDiscovery import MemoryDiscovery
from .DefaultDiscoveryFactory import DefaultDiscoveryFactory

