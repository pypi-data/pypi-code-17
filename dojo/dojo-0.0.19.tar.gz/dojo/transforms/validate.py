from __future__ import absolute_import, print_function, unicode_literals

from jsonschema import validate

from dojo.transform import Transform


class Validate(Transform):

    def __init__(self, schema, *args, **kwargs):
        self.schema = schema
        super(Validate, self).__init__(*args, **kwargs)

    def process(self, row):
        return self.validate_schema(row, self.schema)

    def validate_schema(self, row, schema):
        validate(row, schema)
        return row
