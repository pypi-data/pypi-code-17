# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.dispatch import Signal

transaction_success = Signal(providing_args=["related_obj"])
