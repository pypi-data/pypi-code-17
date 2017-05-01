# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from processengine.models import Process, DataEntry, Execution

class ProcessAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display_name', 'description', 'status')

class ExecutionAdmin(admin.ModelAdmin):
    # ...
    # form = EnumerationChoiceAdminForm

    list_display = ('id', 'begins', 'result', 'status')

admin.site.register(Process, ProcessAdmin)
admin.site.register(Execution, ExecutionAdmin)
admin.site.register(DataEntry)
