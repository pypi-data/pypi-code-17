from django.contrib import admin

from djprogress.models import Progress

class ProgressAdmin(admin.ModelAdmin):
    list_display = ('name', 'current', 'total', 'eta', 'last_updated', 'parent')
    ordering = ('name',)

admin.site.register(Progress, ProgressAdmin)
