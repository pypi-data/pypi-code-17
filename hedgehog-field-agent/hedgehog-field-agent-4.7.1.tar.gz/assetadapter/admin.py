# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from .models import Asset, Command, DeviceManager, ChoiceProperty, IntervalProperty, StringProperty, EnumerationChoice, \
    EnumerationType, Action
from django.contrib import admin

# Register your models here.
class EnumerationChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s (%s)" % (obj.display_name, obj.id)


class ChoicePropertyAdminForm(forms.ModelForm):
    # fields

    class Meta:
        model = ChoiceProperty
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ChoicePropertyAdminForm, self).__init__(*args, **kwargs)
        current_default_unit = self.instance.default_unit
        self.fields['default_unit'].choices = EnumerationChoiceField(queryset=EnumerationChoice.objects.all())


class IntervalPropertyInline(admin.TabularInline):
    model = IntervalProperty
    fk_name = 'owner'
    extra = 1


class ChoicePropertyInline(admin.TabularInline):
    model = ChoiceProperty
    fk_name = 'owner'
    # form = ChoicePropertyAdminForm
    extra = 1


class StringPropertyInline(admin.TabularInline):
    model = StringProperty
    fk_name = 'owner'
    # form = ChoicePropertyAdminForm
    extra = 1


class ActionInline(admin.StackedInline):
    model = Action
    fk_name = 'subject'
    # form = ChoicePropertyAdminForm
    extra = 1


class CommandAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')


class AssetAdmin(admin.ModelAdmin):
    # ...
    # form = EnumerationChoiceAdminForm

    list_display = ('id', 'display_name', 'alias', 'address', 'description')
    inlines = [IntervalPropertyInline, ChoicePropertyInline, StringPropertyInline, ActionInline]


class EnumerationChoiceInline(admin.TabularInline):
    model = EnumerationChoice
    extra = 1


class EnumerationTypeAdmin(admin.ModelAdmin):
    # ...
    inlines = [EnumerationChoiceInline]
    list_display = ('id', 'display_name', 'description')


# admin.site.register(EnumerationChoice)
admin.site.register(EnumerationType, EnumerationTypeAdmin)

admin.site.register(Asset, AssetAdmin)
admin.site.register(Command, CommandAdmin)
admin.site.register(ChoiceProperty)
admin.site.register(IntervalProperty)