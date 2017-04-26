# Create your tasks here
from __future__ import absolute_import, unicode_literals

import logging
from celery import shared_task, Task, app

from orchestrator.celeryapp import app as i
from celery.result import AsyncResult

from orchestrator.settings import VISA_BACKEND
from assetadapter.core import VisaDeviceManager, visa_device_manager

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
logger.setLevel(logging.DEBUG)

@shared_task(serializer='json')
def list_resources():

    logger.debug('TASK >> listing resources ...')

    # from orchestrator.settings import VISA_BACKEND
    # from assetadapter.core import VisaDeviceManager
    #
    # visa_device_manager = VisaDeviceManager(visa_library=VISA_BACKEND)
    result = visa_device_manager.list()

    logger.debug(result)
    return result



@shared_task
def alias(mapping):
    logger.debug('TASK >> alias mapping: %s' % mapping)

    # from orchestrator.settings import VISA_BACKEND
    # from assetadapter.core import VisaDeviceManager
    #
    # visa_device_manager = VisaDeviceManager(visa_library=VISA_BACKEND)
    result = visa_device_manager.alias(resource_mapping=mapping)

    logger.debug(result)
    return result

@shared_task
def read(alias, command):
    logger.debug('TASK >> %s read %s' % (alias, command))

    # from orchestrator.settings import VISA_BACKEND
    # from assetadapter.core import VisaDeviceManager
    #
    # visa_device_manager = VisaDeviceManager(visa_library=VISA_BACKEND)
    result = visa_device_manager.read(alias=alias, command=command)

    logger.debug(result)
    return result

@shared_task
def write(alias, command):
    logger.debug('TASK >> %s write %s' % (alias, command))

    # from orchestrator.settings import VISA_BACKEND
    # from assetadapter.core import VisaDeviceManager
    #
    # visa_device_manager = VisaDeviceManager(visa_library=VISA_BACKEND)
    visa_device_manager.write(alias=alias, command=command)

@shared_task
def query(alias, command):
    logger.debug('TASK >> %s query %s' % (alias, command))

    # from orchestrator.settings import VISA_BACKEND
    # from assetadapter.core import VisaDeviceManager
    #
    # visa_device_manager = VisaDeviceManager(visa_library=VISA_BACKEND)


    # visa_device_manager.alias({ alias})
    result = visa_device_manager.query(alias=alias, command=command)

    logger.debug(result)
    return result

@shared_task
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task {0} raised exception: {1!r}\n{2!r}'.format(uuid, exc, result.traceback))