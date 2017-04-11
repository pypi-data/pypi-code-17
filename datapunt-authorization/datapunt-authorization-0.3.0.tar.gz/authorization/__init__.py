"""
    authorization
    ~~~~~~~~~~~~~

    This package provides an implementation of the Datapunt authorization
    model.
"""

import authorization_levels as levels
from .map import AuthzMap

__all__ = ('levels', 'AuthzMap')
