from django.contrib import admin

from models import Log


class LogAdmin(admin.ModelAdmin):
    list_filter = ['tag', 'status', 'level']
    raw_id_fields = ('user',)
    list_display = ['title', 'tag', 'level', 'user','status', 'created_at']
    search_fields = ('user', )


admin.site.register(Log, LogAdmin)