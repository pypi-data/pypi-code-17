from django.contrib import admin
# from django.utils.translation import ugettext_lazy as _
from .models import ComparisonProduct


class ComparisonProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'variant', 'customer', 'site', 'added')
    search_fields = ('product', 'variant', 'customer')
    raw_id_fields = ('product', 'variant', 'customer')
    date_hierarchy = 'added'


admin.site.register(ComparisonProduct, ComparisonProductAdmin)
