# -*- coding: utf-8 -*-
"""
    pip_services_commons.validate.FilterParamsSchema
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    FilterParams schema implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..convert.TypeCode import TypeCode
from .MapSchema import MapSchema

class FilterParamsSchema(MapSchema):

    def __init__(self):
        super(FilterParamsSchema, self).__init__(TypeCode.String, None)
