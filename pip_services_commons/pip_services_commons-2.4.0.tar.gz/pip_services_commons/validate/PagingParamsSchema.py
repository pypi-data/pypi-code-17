# -*- coding: utf-8 -*-
"""
    pip_services_commons.validate.PagingParamsSchema
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    PagingParams schema implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..convert.TypeCode import TypeCode
from .ObjectSchema import ObjectSchema

class PagingParamsSchema(ObjectSchema):

    def __init__(self):
        super(PagingParamsSchema, self).__init__()
        self.with_optional_property('skip', TypeCode.Long)
        self.with_optional_property('take', TypeCode.Long)
        self.with_optional_property('total', TypeCode.Boolean)
