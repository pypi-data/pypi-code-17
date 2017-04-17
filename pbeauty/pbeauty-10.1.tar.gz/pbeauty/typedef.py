# -*- coding: utf-8 -*-

class Lable:
    LABLE_OPTIONAL = 'optional'
    LABLE_REQUIRED = 'required'
    LABLE_REPEATED = 'repeated'
    LABLE_ENUM = (LABLE_OPTIONAL, LABLE_REQUIRED, LABLE_REPEATED)


class Types:
    BASICAL_TYPES = (
            'int',
            'int32', 'uint32',
            'int64', 'uint64',
            'sint32', 'sint64',
            'fixed32', 'fixed64',
            'sfixed32', 'sfixed64',
            'bool',
            'string', 'bytes',
            'double', 'float',
    )

    @staticmethod
    def IsBasicalType(type):
        return type in Types.BASICAL_TYPES


