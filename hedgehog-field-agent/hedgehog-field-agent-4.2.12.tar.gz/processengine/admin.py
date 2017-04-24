# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from processengine.models import Process, DataEntry

admin.site.register(Process)
admin.site.register(DataEntry)
