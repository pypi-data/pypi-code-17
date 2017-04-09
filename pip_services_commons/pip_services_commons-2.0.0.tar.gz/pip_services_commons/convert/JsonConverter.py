# -*- coding: utf-8 -*-
"""
    pip_services_commons.convert.JsonConverter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Json conversion utilities
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import json

from .RecursiveMapConverter import RecursiveMapConverter

class JsonConverter(object):

    @staticmethod
    def from_json(value):
        if value == None:
            return None

        value = json.loads(value)

    @staticmethod
    def to_json(value):
        if value == None:
            return None

        return json.dumps(value)

    @staticmethod
    def to_nullable_map(value):
        if value == None:
            return None

        # Parse JSON
        try:
            value = json.loads(value)
            return RecursiveMapConverter.to_nullable_map(value)
        except:
            return None

    @staticmethod
    def to_map(value):
        result = JsonConverter.to_nullable_map(value)
        return result if result != None else {}

    @staticmethod
    def to_map_with_default(value, default_value):
        result = JsonConverter.to_nullable_map(value)
        return result if result != None else default_value
