from django.contrib import admin
from models import UrlRedirect


class UrlAdmin(admin.ModelAdmin):
    list_filter = ['status']
    list_display = ['url_source', 'url_destination', 'views', 'status', 'date_initial_validity','date_end_validity']
    search_fields = ('url_source', 'url_destination',)


admin.site.register(UrlRedirect,UrlAdmin)