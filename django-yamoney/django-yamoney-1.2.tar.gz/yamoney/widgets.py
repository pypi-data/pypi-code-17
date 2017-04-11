# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import forms
from django.utils.encoding import force_text


class LowercaseHiddenInput(forms.HiddenInput):
    def _format_value(self, value):
        value = super(LowercaseHiddenInput, self)._format_value(value)
        return force_text(value).lower()
