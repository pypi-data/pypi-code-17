# -*- coding: utf-8 -*-
"""
    pip_services_commons.data.DataPage
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Data page implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class DataPage(object):
    """
    Represents a page with optional total record counter
    """

    total = None
    data = None

    def __init__(self, data, total = None):
        self.data = data
        self.total = total

    def to_json(self):
        return {
            'data': self.data,
            'total': self.total
        }

    @staticmethod
    def from_json(value):
        if not isinstance(value, dict):
            return value

        data = value['data'] if 'data' in value else []
        total = value['total'] if 'total' in value else None
        return DataPage(data, total)