from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import AuditEvent

#@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tstamp_beg', 'duration',
                    'severity', 'outcome',
                    'initiator_name', 'initiator_id',
                    'target_name', 'target_id',
                    'details',
                    'src_ip_addr',
                    'src_country', 'src_city'
                   )
    list_filter = ('name', 'outcome', 'severity', 'src_country')
    date_hierarchy = 'tstamp_beg'
    readonly_fields = ('tstamp_beg', 'name', 'outcome', 'severity', 'tstamp_end', 'duration',
                    'src_ip_addr', 'details',
                    'initiator_name', 'initiator_id',
                    'target_name', 'target_id',
                    'error_msg',
                    'src_city', 'src_country', 'src_latitude', 'src_longitude')
    fieldsets = (
                        (_("What"), {'fields': (('name', 'outcome', 'severity', 'error_msg'),)}),

                        (_("When"), {'classes': ('grp-collapse grp-open',),
                                     'fields': (('tstamp_beg', 'duration', 'tstamp_end'),)}),
                        (_('Who & where'), {'classes': ('grp-collapse grp-open',), 'fields': (('initiator_name',),
                                                     ('target_name',),
                                                     'src_ip_addr',
                                                     ('src_country', 'src_city'),
                                                     ('src_latitude', 'src_longitude'))}),
                        (_("More"), {'classes': ('grp-collapse grp-open',), 'fields': ('details', 'comment')})
                )
    search_fields = ('initiator', 'target')

    def has_add_permission(self, request):
        return False