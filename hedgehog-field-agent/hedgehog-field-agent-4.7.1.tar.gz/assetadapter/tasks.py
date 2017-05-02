# Create your tasks here
from __future__ import absolute_import, unicode_literals

import logging

from celery import shared_task
from celery.result import AsyncResult
from celery.utils.log import get_task_logger

from visacore.core import visa_device_manager

logger = get_task_logger(__name__)
logger.setLevel(logging.DEBUG)

from celery import Task
from celery.signals import task_prerun, task_postrun


# class VisaTask(Task):
#     def on_failure(self, exc, task_id, args, kwargs, einfo):
#         super(VisaTask, self).on_failure(exc, task_id, args, kwargs, einfo)
#
#     def on_success(self, retval, task_id, args, kwargs):
#         super(VisaTask, self).on_success(retval, task_id, args, kwargs)


# @task_prerun.connect
# def task_sent_handler(sender=None, headers=None, body=None, **kwargs):
#     # information about task are located in headers for task messages
#     # using the task protocol version 2.
#     info = headers if 'task' in headers else body
#     print('after_task_publish for task id {info[id]}'.format(
#         info=info,
#     ))
#
# @task_postrun.connect
# def task_sent_handler(sender=None, headers=None, body=None, **kwargs):
#     # information about task are located in headers for task messages
#     # using the task protocol version 2.
#     info = headers if 'task' in headers else body
#     print('after_task_publish for task id {info[id]}'.format(
#         info=info,
#     ))


@shared_task(serializer='json')
def list_resources():
    logger.debug('TASK >> listing resources ...')

    # from orchestrator.settings import VISA_BACKEND
    # from processengine.core import VisaDeviceManager
    #
    # visa_device_manager = VisaDeviceManager(visa_library=VISA_BACKEND)
    result = visa_device_manager.list()

    logger.debug(result)
    return result


@shared_task
def alias(mapping):
    logger.debug('TASK >> alias mapping: %s' % mapping)

    # from orchestrator.settings import VISA_BACKEND
    # from processengine.core import VisaDeviceManager
    #
    # visa_device_manager = VisaDeviceManager(visa_library=VISA_BACKEND)
    result = visa_device_manager.alias(resource_mapping=mapping)

    logger.debug(result)
    return result


@shared_task
def read(alias, command):
    logger.debug('TASK >> %s read %s' % (alias, command))

    # from orchestrator.settings import VISA_BACKEND
    # from processengine.core import VisaDeviceManager
    #
    # visa_device_manager = VisaDeviceManager(visa_library=VISA_BACKEND)
    result = visa_device_manager.read(alias=alias, command=command)

    logger.debug(result)
    return result


@shared_task
def write(alias, command):
    logger.debug('TASK >> %s write %s' % (alias, command))

    # from orchestrator.settings import VISA_BACKEND
    # from processengine.core import VisaDeviceManager
    #
    # visa_device_manager = VisaDeviceManager(visa_library=VISA_BACKEND)
    visa_device_manager.write(alias=alias, command=command)


@shared_task
def query(alias, command):
    logger.debug('TASK >> %s query %s' % (alias, command))

    # from orchestrator.settings import VISA_BACKEND
    # from processengine.core import VisaDeviceManager
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