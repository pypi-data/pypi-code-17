# Create your tasks here
from __future__ import absolute_import, unicode_literals

import json
import logging
from celery import shared_task, Task

import processengine
from assetadapter.tasks import alias, write, query
from processengine.models import Execution, PENDING, INITIALIZED, RUNNING, DONE, FAILURE

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class PersistentQueryTask(Task):
    def on_success(self, retval, task_id, args, kwargs):

        super(PersistentQueryTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        super(PersistentQueryTask, self).on_failure(exc, task_id, args, kwargs)



@shared_task(serializer='json')
def execute_process(executor_id, local_variables):
    process= processengine.models.Process.objects.get(pk=executor_id)
    executionResult = process.run(variables=local_variables)

    return executionResult