# !/usr/bin/env python
# encoding:UTF-8

from django.contrib import admin
from dynamic_preferences.models import GlobalPreferenceModel, UserPreferenceModel
from django import forms


class PreferenceChangeListForm(forms.ModelForm):
    """
    A form that integrate dynamic-preferences into django.contrib.admin
    """
    # Me must use an acutal model field, so we use raw_value. However, 
    # instance.value will be displayed in form.
    raw_value = forms.CharField()

    def is_multipart(self):
        """
        TODO: capire come fixare meglio l'accrocchio del multipart-encoded
        Returns True if the form needs to be multipart-encoded, i.e. it has
        FileInput. Otherwise, False.
        """
        return True

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')
        # self.raw_value = self.instance.preference.setup_field()
        # self.base_fields = {'raw_value': self.instance.preference.setup_field()}
        # self.declared_fields = self.base_fields
        super(PreferenceChangeListForm, self).__init__(*args, **kwargs)
        self.fields['raw_value'] = self.instance.preference.setup_field()

    def save(self, *args, **kwargs):
        self.cleaned_data['raw_value'] = self.instance.preference.serializer.serialize(self.cleaned_data['raw_value'])
        return super(PreferenceChangeListForm, self).save(*args, **kwargs)


class GlobalPreferenceChangeListForm(PreferenceChangeListForm):
    class Meta:
        model = GlobalPreferenceModel


class UserPreferenceChangeListForm(PreferenceChangeListForm):
    class Meta:
        model = UserPreferenceModel


class DynamicPreferenceAdmin(admin.ModelAdmin):
    changelist_form = PreferenceChangeListForm
    readonly_fields = ('section', 'name', 'value', 'help')
    fields = ("raw_value",)
    list_display = ['section', 'name', 'raw_value', 'help']
    list_display_links = ['name',]
    list_editable = ('raw_value',)
    #search_fields = ['section', 'name', 'help']
    search_fields = []
    list_filter = ('section',)
    ordering = ('section', 'name')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        return []

    def get_changelist_form(self, request, **kwargs):
        return self.changelist_form

    # def get_search_results(self, request, queryset, search_term):
    #     queryset_original = queryset
    #     queryset, use_distinct = super(DynamicPreferenceAdmin, self).get_search_results(request, queryset, search_term)
    #     if not len(queryset):
    #         # self.message_user(request, "No result found for: '" + search_term + "'", messages.SUCCESS)
    #         queryset = queryset_original
    #     return queryset, use_distinct


class GlobalPreferenceAdmin(DynamicPreferenceAdmin):
    form = GlobalPreferenceChangeListForm
    changelist_form = GlobalPreferenceChangeListForm


admin.site.register(GlobalPreferenceModel, GlobalPreferenceAdmin)


class UserPreferenceAdmin(DynamicPreferenceAdmin):
    form = UserPreferenceChangeListForm
    changelist_form = UserPreferenceChangeListForm
    list_display = ['user'] + DynamicPreferenceAdmin.list_display
    search_fields = ['user__username'] + DynamicPreferenceAdmin.search_fields


admin.site.register(UserPreferenceModel, UserPreferenceAdmin)
