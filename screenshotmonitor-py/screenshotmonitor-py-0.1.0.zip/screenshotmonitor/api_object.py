# -*- coding: utf-8 -*-
"""

"""


class SSMObject(object):
    def __init__(self):
        self._api = None

    @classmethod
    def from_json_dict(cls, d):
        """Given a dictionary object serialized from JSON, returns an instance of this object"""
        raise NotImplementedError()
