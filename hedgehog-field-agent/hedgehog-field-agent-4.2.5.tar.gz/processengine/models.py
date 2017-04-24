# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json

import datetime

import django
from django.db import models

# Create your models here.
from assetadapter.models import Asset, Property, Command, Entity, EnumerationChoice


class Process(Entity):
    name = models.CharField(max_length=200)


class Variable(models.Model):
    value = models.CharField(max_length=200)
    binding = models.ForeignKey(Property, on_delete=models.CASCADE)
    scope = models.ForeignKey(Process, related_name='variables', on_delete=models.CASCADE)


class Action(models.Model):
    binding = models.ForeignKey(Command, on_delete=models.CASCADE)
    scope = models.ForeignKey(Process, related_name='hooked_actions', on_delete=models.CASCADE)
    domain = models.CharField(max_length=200)

class DataEntry(models.Model):
    domain = models.CharField(max_length=200)
    unit = models.ForeignKey(EnumerationChoice, on_delete=models.CASCADE, null=True, blank=True, default=None)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=django.utils.timezone.now)
    process = models.ForeignKey(Process, on_delete=models.CASCADE, null=True, blank=True, default=None)
    data = models.BinaryField()

    def __str__(self):
        return ('[' + self.domain + '|' + self.asset + '|' + self.process + '|' + self.timestamp + ']: ' + json.dumps(
            self.data)).encode('utf8')
