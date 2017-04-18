# -*- coding: utf-8 -*-
"""
    pip_services_commons.validate.ObjectSchema
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Object schema implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .Schema import Schema
from .ValidationResultType import ValidationResultType
from .ValidationResult import ValidationResult
from .PropertySchema import PropertySchema
from ..reflect.ObjectReader import ObjectReader

class ObjectSchema(Schema):
    properties = None
    is_allow_undefined = None

    def __init__(self):
        self.is_allow_undefined = False

    def allow_undefined(self, value):
        self.is_allowUndefined = value
        return self

    def with_property(self, schema):
        self.properties = self.properties if self.properties != None else []
        self.properties.append(schema)
        return self

    def with_required_property(self, name, typ, *rules):
        self.properties = self.properties if self.properties != None else []
        schema = PropertySchema(name, typ)
        schema.rules = rules
        schema.make_required()
        return self.with_property(schema)

    def with_optional_property(self, name, typ, *rules):
        self.properties = self.properties if self.properties != None else []
        schema = PropertySchema(name, typ)
        schema.rules = rules
        schema.make_optional()
        return self.with_property(schema)

    def _perform_validation(self, path, value, results):
        super(ObjectSchema, self)._perform_validation(path, value, results)

        if value == None:
            return

        name = path if path != None else "value"
        properties = ObjectReader.get_properties(value)

        # Process defined properties
        if self.properties != None:
            for property_schema in self.properties:
                processed_name = None

                for (key, value) in properties.items():
                    # Find properties case insensitive
                    if property_schema.name != None and key.lower() == property_schema.name.lower():
                        property_schema._perform_validation(path, value, results)
                        processed_name = key
                        break

                if processed_name == None:
                    property_schema._perform_validation(path, None, results)
                else:
                    del properties[processed_name]

        # Process unexpected properties
        for (key, value) in properties.items():
            property_path = key if path == None or len(path) == 0 else path + "." + key

            results.append(
                ValidationResult(
                    property_path,
                    ValidationResultType.Warning,
                    "UNEXPECTED_PROPERTY",
                    name + " contains unexpected property " + str(key),
                    None,
                    key
                )
            )
