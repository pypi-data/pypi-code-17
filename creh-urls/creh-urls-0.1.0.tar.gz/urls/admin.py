from django.contrib import admin
from models import UrlRedirect


class UrlAdmin(admin.ModelAdmin):
    list_filter = ['status']
    list_display = ['url_source', 'url_destination', 'views', 'status', 'created_at','updated_at']
    search_fields = ('url_source', 'url_destination',)


admin.site.register(UrlRedirect,UrlAdmin)