# -*- coding: utf-8 -*-
"""
    pip_services_commons.data.PagingParams
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Data paging parameters implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..convert.IntegerConverter import IntegerConverter
from ..convert.BooleanConverter import BooleanConverter
from .AnyValueMap import AnyValueMap

class PagingParams(object):
    """
    Stores data paging parameters
    """

    skip = None
    take = None
    total = True

    def __init__(self, skip = None, take = None, total = True):
        self.skip = IntegerConverter.to_nullable_integer(skip)
        self.take = IntegerConverter.to_nullable_integer(take)
        self.total = BooleanConverter.to_boolean_with_default(total, True)

    def get_skip(self, min_skip):
        if self.skip == None:
            return min_skip
        if self.skip < min_skip:
            return min_skip
        return self.skip 

    def get_take(self, max_take):
        if self.take == None:
            return max_take
        if self.take < 0:
            return 0
        if self.take > max_take:
            return max_take
        return self.take

    def has_total(self):
        return self.total

    def to_json(self):
        return {
            'skip': self.skip,
            'take': self.take,
            'total': self.total
        }

    @staticmethod
    def from_json(value):
        if not isinstance(value, dict):
            return value
        
        skip = value['skip'] if 'skip' in value else None
        take = value['take'] if 'take' in value else None
        total = value['total'] if 'total' in value else None
        return PagingParams(skip, take, total)

    @staticmethod
    def from_value(value):
        if isinstance(value, PagingParams):
            return value
        if isinstance(value, AnyValueMap):
            return PagingParams.from_map(value)
        
        map = AnyValueMap.from_value(value)
        return PagingParams.from_map(map)

    @staticmethod
    def from_tuples(*tuples):
        map = AnyValueMap.from_tuples_array(tuples)
        return PagingParams.from_map(map)

    @staticmethod
    def from_map(map):
        skip = map.get_as_nullable_integer("skip")
        take = map.get_as_nullable_integer("take")
        total = map.get_as_nullable_boolean("total")
        return PagingParams(skip, take, total)
