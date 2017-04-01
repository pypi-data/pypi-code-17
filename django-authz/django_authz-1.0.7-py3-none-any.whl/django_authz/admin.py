# -*- coding:utf-8 -*-                                                         #

#===============================================================================
# Copyright (C) 2017 Dariusz L. Leonarski
# All Rights Reserved
# This software is protected under the terms of the proprietary license.
#===============================================================================

from django.contrib import admin
from .models import Role, Grant

class AuthzAdmin(admin.ModelAdmin):
    def get_queryset(self, request, *args, **kwargs):
        return self.model.authz_get_queryset(request)


class InlineGrant(admin.TabularInline):
    model = Grant
    fields = ('trustee_ctype', 'trustee_objid', 'target_ctype', 'target_objid', 'reason', 'inactive_till')
    extra = 0

    def add_view(self, request, **kwargs):
        self.readonly_fields = []
        return super(InlineGrant, self).add_view(request, **kwargs)

    def change_view(self, request, obj_id, **kwargs):
        self.readonly_fields = ('trustee_ctype', 'trustee_objid',
                                'target_ctype', 'target_objid',
                                'reason', 'inactive_till')
        return super(InlineGrant, self).change_view(request, obj_id, **kwargs)
    related_lookup_fields = {'generic': [
                                            ['trustee_ctype', 'trustee_objid'],
                                            ['target_ctype', 'target_objid']
                                         ]
                            }


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'description', 'active', 'implemented')
    list_filter = ('active',)
    readonly_fields = ('implemented', 'details')
    inlines = (InlineGrant,)

    def change_view(self, request, obj_id, **kwargs):
        self.readonly_fields = ('implemented', 'name', 'details')
        return super(RoleAdmin, self).change_view(request, obj_id, **kwargs)


@admin.register(Grant)
class GrantAdmin(admin.ModelAdmin):
    list_display = ('role', 'trustee', 'target', 'reason', 'inactive_till')
    related_lookup_fields = {'generic': [
                                            ['trustee_ctype', 'trustee_objid'],
                                            ['target_ctype', 'target_objid']
                                         ]
                            }
    #  In case Grappelli is in use
    autocomplete_lookup_fields = related_lookup_fields
