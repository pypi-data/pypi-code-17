# -*- coding: utf-8 -*-
"""
    pip_services_commons.refer.__init__
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    References module initialization
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

__all__ = [
    'Descriptor',
    'IReferenceable', 'IUnreferenceable', 'IReferences',
    'ReferenceException', 'Referencer', 'Reference',
    'References', 'DependencyResolver'
]

from .Descriptor import Descriptor
from .IReferenceable import IReferenceable
from .IUnreferenceable import IUnreferenceable
from .IReferences import IReferences
from .ReferenceException import ReferenceException
from .Referencer import Referencer
from .Reference import Reference
from .References import References
from .DependencyResolver import DependencyResolver