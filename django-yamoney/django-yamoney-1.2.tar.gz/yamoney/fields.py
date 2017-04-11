# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import dateutil.parser
from django import forms


class DateTimeISO6801Field(forms.DateTimeField):
    def strptime(self, value, format):
        return dateutil.parser.parse(value)
