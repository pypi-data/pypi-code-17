# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import threading

import logging

import datetime
from django.db import models
# Create your models here.
from visa import ResourceManager

from assetadapter.tasks import list_resources, error_handler


class Entity(models.Model):
    display_name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.display_name.encode('utf8')

class EnumerationType(Entity):
    def choices(self):
        return self.choice_set.all()

class EnumerationChoice(models.Model):
    value = models.CharField(max_length=200)
    owner = models.ForeignKey(EnumerationType, on_delete=models.CASCADE)

    def __str__(self):
        return self.value.encode('utf8')




class Asset(Entity):
    alias = models.CharField(max_length=200, null=True, blank=True, default=None)
    address = models.CharField(max_length=200)

    # def __str__(self):
    #     return self.alias

class Command(models.Model):
    code = models.CharField(max_length=200)
    subject = models.ForeignKey(Asset, related_name='actions', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.code.encode('utf8')

class Property(Entity):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(Asset, related_name='properties', on_delete=models.CASCADE)
    unit_choices = models.ForeignKey(EnumerationType, on_delete=models.CASCADE, null=True, blank=True, default = None)
    default_unit = models.ForeignKey(EnumerationChoice, on_delete=models.CASCADE, null=True, blank=True, default = None)
    type = models.CharField(max_length=200, default='string', choices=((u'string', u'string'), (u'interval', u'interval'), (u'choice', u'choice')))
    getter_command = models.OneToOneField(Command, related_name='getter_command', on_delete=models.CASCADE, null=True, blank=True)
    setter_command = models.OneToOneField(Command, related_name='setter_command', on_delete=models.CASCADE, null=True, blank=True)

    # def __str__(self):
    #     return self.name

class StringProperty(Property):
    default_value = models.CharField(max_length=200, null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super(StringProperty, self).__init__(*args, **kwargs)
        StringProperty._meta.get_field('type').default = 'string'

class ChoiceProperty(Property):
    value_choices = models.ForeignKey(EnumerationType, on_delete=models.CASCADE)
    default_value = models.ForeignKey(EnumerationChoice, on_delete=models.CASCADE, null=True, blank=True, default = None)


    def __init__(self, *args, **kwargs):
        super(ChoiceProperty, self).__init__(*args, **kwargs)
        ChoiceProperty._meta.get_field('type').default = 'choice'

    def get_value(self):
        return EnumerationChoice.get(id=self.choice)

class IntervalProperty(Property):
    minimum = models.FloatField()
    maximum = models.FloatField()
    default_value = models.FloatField()

    def __init__(self, *args, **kwargs):
        super(IntervalProperty, self).__init__(*args, **kwargs)
        IntervalProperty._meta.get_field('type').default = 'interval'

    def get_value(self):
        return self.value


class DeviceManager():
    def active_resources(self):
        result = list_resources.apply_async((), link_error=error_handler.s())
        resources = result.get(timeout=1)
        if resources == None:
            resources = []
        connected_assets = Asset.objects.filter(address__in=resources)
        return connected_assets

    def inactive_resources(self):
        result = list_resources.apply_async((), link_error=error_handler.s())
        resources = result.get(timeout=1)

        if resources == None:
            resources = []
        disconnected_assets = Asset.objects.exclude(address__in=resources).all()
        return disconnected_assets

    def unknown_resources(self):
        result = list_resources.apply_async((), link_error=error_handler.s())
        resources = result.get(timeout=1)
        if resources == None:
            resources = []
        asset_addresses = Asset.objects.all().values_list('address')

        result = [item for item in resources if item not in asset_addresses]

        return result