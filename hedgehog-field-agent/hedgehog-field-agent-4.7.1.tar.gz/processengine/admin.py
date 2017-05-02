# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
import processengine
from processengine.models import DataEntry, Execution

class ProcessAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display_name', 'description', 'status')

class ExecutionAdmin(admin.ModelAdmin):
    # ...
    # form = EnumerationChoiceAdminForm

    list_display = ('id', 'begins', 'result', 'status')

admin.site.register(processengine.models.Process, ProcessAdmin)
admin.site.register(Execution, ExecutionAdmin)
admin.site.register(DataEntry)
