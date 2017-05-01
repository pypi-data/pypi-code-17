# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json

import datetime

import django
from django.db import models

# Create your models here.
from django_celery_results.models import TaskResult

from assetadapter.models import Asset, Property, Command, Entity, EnumerationChoice

PENDING = 'pending'
INITIALIZED = 'initialized'
RUNNING = 'running'
DISABLED = 'disabled'
DONE = 'done'
FAILURE = 'failure'

STATUS_CHOICES = (
    (PENDING, 'Függőben'),
    (INITIALIZED, 'Inicializálva'),
    (RUNNING, 'Fut'),
    (DISABLED, 'Inaktív'),
    (DONE, 'Végzett'),
    (FAILURE, 'Hiba')
)

class Process(Entity):
    name = models.CharField(max_length=200)
    status = models.CharField(choices=STATUS_CHOICES, default=PENDING, max_length=200)
    input_parameters = models.ManyToManyField(Property, related_name='input_parameters', null=True, blank=True, default=None)
    output_parameters = models.ManyToManyField(Property, related_name='output_parameters', null=True, blank=True, default=None)

    def run(self, variables={}, timestamp=datetime.datetime.now()):
        execution = Execution.objects.create(executor=self, begins=timestamp, status=RUNNING)
        # local_variables = {}
        # for input in self.input_parameters:
        #     local_variables[input.name] = variables[input.name] if variables[input.name] is not None else input.get_default_value()
        #
        # for



        return execution


class Execution(models.Model):
    executor = models.ForeignKey(Process, related_name='executions', on_delete=models.CASCADE)
    begins = models.DateTimeField(null=True, blank=True, default=None)
    status = models.CharField(choices=STATUS_CHOICES, default=PENDING, max_length=200)
    result = models.ForeignKey(TaskResult, on_delete=models.CASCADE, null=True, blank=True, default=None)


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
