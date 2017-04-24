# Create your tasks here
from __future__ import absolute_import, unicode_literals

import logging
from celery import shared_task, Task, app
from orchestrator.celeryapp import app as i
from celery.result import AsyncResult


# from celery.utils.log import get_task_logger
# logger = get_task_logger()
# logger.setLevel(logging.INFO)

from orchestrator.settings import VISA_BACKEND
from assetadapter.core import VisaDeviceManager

visa_device_manager = VisaDeviceManager(visa_library=VISA_BACKEND)


@shared_task(serializer='json')
def list_resources():
    return visa_device_manager.list()

@shared_task
def alias(mapping):
    return visa_device_manager.alias(resource_mapping=mapping)

@shared_task
def read(alias, command):
    return visa_device_manager.read(alias=alias, command=command)

@shared_task
def write(alias, command):
    visa_device_manager.write(alias=alias, command=command)

@shared_task
def query(alias, command):
    return visa_device_manager.query(alias=alias, command=command)

@shared_task
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task {0} raised exception: {1!r}\n{2!r}'.format(uuid, exc, result.traceback))