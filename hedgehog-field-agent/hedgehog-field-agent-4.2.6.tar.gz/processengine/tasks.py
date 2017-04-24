# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task, Task


class PersistentQueryTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        super(PersistentQueryTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        super(PersistentQueryTask, self).on_failure(exc, task_id, args, kwargs)


def execute_process(variables):
    subtasks = [RefreshFeedTask.subtask(kwargs={"feed_url": url}) for url in urls]