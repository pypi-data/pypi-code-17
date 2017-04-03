# -*- coding: utf-8 -*-
"""
Override django.core.serializers.json.Serializer which renders our MoneyType as float.
"""
from __future__ import unicode_literals
import json
from django.core.serializers.json import DjangoJSONEncoder, Serializer as DjangoSerializer
from django.core.serializers.json import Deserializer
from .money_maker import AbstractMoney

__all__ = ['Serializer', 'Deserializer']


class JSONEncoder(DjangoJSONEncoder):
    """
    Money type aware JSON encoder for reciprocal usage, such as import/export/dumpdata/loaddata.
    """
    def default(self, obj):
        if isinstance(obj, AbstractMoney):
            return float(obj)
        return super(JSONEncoder, self).default(obj)


class Serializer(DjangoSerializer):
    """
    Money type aware JSON serializer.
    """
    def end_object(self, obj):
        # self._current has the field data
        indent = self.options.get("indent")
        if not self.first:
            self.stream.write(",")
            if not indent:
                self.stream.write(" ")
        if indent:
            self.stream.write("\n")
        json.dump(self.get_dump_object(obj), self.stream, cls=JSONEncoder, **self.json_kwargs)
        self._current = None
