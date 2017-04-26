from django.contrib import admin

from .models import Room


# @admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'created_at', 'created_by',)
    list_display_links = ('name',)
    list_filter = ('name',)
    filter_horizontal = ('users',)

admin.site.register(Room, RoomAdmin)
