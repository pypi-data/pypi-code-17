# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import logging

import django
import viewflow
from django.db import models
# Create your models here.
from django.utils import timezone
from django_celery_results.models import TaskResult

import processengine
from assetadapter.models import Asset, Property, Entity, EnumerationChoice
from assetadapter.tasks import write, alias

from viewflow.models import Process as VfProcess

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


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class AlertProcess(VfProcess):
    text = models.CharField(max_length=150)
    approved = models.BooleanField(default=False)
    timestamp = models.DateTimeField(null=True, blank=True, default=None)

class InputParametersEntity(models.Model):
    # variables = models.TextField(max_length=1000, default=None, null=True, blank=True)
    # values = models.TextField(max_length=1000, default=None, null=True, blank=True)
    # properties = models.TextField(max_length=1000, default=None, null=True, blank=True)
    pass

class DataVolume(models.Model):
    pass
# class ExectionUnit(models.Model):


class ObserverProcess(VfProcess):
    asset = models.ForeignKey(Asset)
    # input_parameters = models.ForeignKey(InputParametersEntity, on_delete=models.CASCADE)
    sampling = models.IntegerField(default=1, null=True, blank=True, help_text='s')
    actions = models.TextField(max_length=1000, default=None, null=True, blank=True)

    @property
    def address(self):
        return self.asset.address

    @property
    def sampling(self):
        return self.sampling

    @property
    def actions(self):
        return self.actions

    # @property
    # def variables(self):
    #     return self.input_parameters.variables
    #
    # @property
    # def properties(self):
    #     return self.input_parameters.properties
    #
    # @property
    # def values(self):
    #     return self.input_parameters.values

class Process(Entity):
    name = models.CharField(max_length=200)
    status = models.CharField(choices=STATUS_CHOICES, default=PENDING, max_length=200)
    input_parameters = models.ManyToManyField(Property, related_name='input_parameters', null=True, blank=True, default=None)
    output_parameters = models.ManyToManyField(Property, related_name='output_parameters', null=True, blank=True, default=None)
    parameters = models.TextField(null=True, default=None, editable=False)

    def last_execution(self):
        return Execution.objects.latest('begins')

    def run(self, variables={}, timestamp=timezone.now()):


        execution = Execution.objects.create(executor=self, begins=timestamp, status=PENDING)
        logger.info('Starting new execution %s form process %s' % (execution.id, self.id))

        for key, value in json.loads(self.parameters).items():
            try:
                if key not in variables:
                    variables[key] = value
            except Exception as ex:
                pass
                # .error('Parameter %s could not set to %s' % (key, value))
        logger.debug('Setup and persist parameters: ' + variables)
        execution.parameters = variables
        execution.status = INITIALIZED
        execution.save()

        logger.debug('Collect asset mapping ...')
        mapping = {}
        for property in self.input_parameters.all():
            asset_alias = property.owner.alias
            address = property.owner.address
            mapping[asset_alias] = address
        logger.debug(mapping)

        chain = alias.s(mapping)


        # r = alias.delay(mapping)
        # logger.debug(str(r.get()) + ' items connected')


        execution.status = RUNNING
        execution.save()

        try:

            logger.debug('Start VISA transaction ...')
            for property in self.input_parameters.all():
                asset_alias = property.owner.alias
                logger.debug('- Resolve (value=%s,unit=%s)' % (property.name, (property.default_unit.value if property.default_unit is not None else '')))
                command = property.setter(json.loads(variables)[property.name][0], (property.default_unit.value if property.default_unit is not None else ''))
                logger.debug('- Write %s to %s' % (command, asset_alias))

                # chain = chain | \
                write.s(asset_alias, command)

                execution.status = DONE
                execution.save()
        except Exception as ex:
            logger.exception('Parameter setup')

            execution.status = FAILURE
            execution.save()

            self.status = FAILURE
            self.save()

        # chain()


class Execution(models.Model):
    executor = models.ForeignKey(Process, related_name='executions', on_delete=models.CASCADE)
    begins = models.DateTimeField(null=True, blank=True, default=None)
    status = models.CharField(choices=STATUS_CHOICES, default=PENDING, max_length=200)
    result = models.ForeignKey(TaskResult, on_delete=models.CASCADE, null=True, blank=True, default=None)
    parameters = models.TextField(null=True, default=None, editable=False)


class Variable(models.Model):
    value = models.CharField(max_length=200)
    binding = models.ForeignKey(Property, on_delete=models.CASCADE)
    scope = models.ForeignKey(Process, related_name='variables', on_delete=models.CASCADE)


# class Action(models.Model):
#     binding = models.ForeignKey(Command, on_delete=models.CASCADE)
#     scope = models.ForeignKey(Process, related_name='hooked_actions', on_delete=models.CASCADE)
#     domain = models.CharField(max_length=200)

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
