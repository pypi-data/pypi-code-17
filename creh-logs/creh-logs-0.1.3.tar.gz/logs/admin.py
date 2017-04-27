from django.contrib import admin

from models import Log


class LogAdmin(admin.ModelAdmin):

    list_display = ['title', 'tag', 'level', 'status']


admin.site.register(Log, LogAdmin)