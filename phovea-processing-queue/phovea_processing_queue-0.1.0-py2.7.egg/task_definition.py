from __future__ import absolute_import, print_function
import functools
import redis
from celery.result import AsyncResult
from celery import Task
from celery.utils.log import get_task_logger


_log = get_task_logger(__name__)


def _create_celery():
  from celery import Celery
  from phovea_server.plugin import list as list_plugins
  from phovea_server.config import view as config_view

  # set configured registry
  plugins = list_plugins('processing-task')
  cc = config_view('phovea_processing_queue')
  print(cc.get('celery.name'),
        cc.get('celery.broker'),
        cc.get('celery.backend'))

  def _map(p):
    # print 'add processing tasks: ' + p.module
    _log.info('add processing task: %s', p.module)
    return p.module

  task_modules = map(_map, plugins)

  app = Celery(
      cc.get('celery.name'),
      broker=cc.get('celery.broker'),
      backend=cc.get('celery.backend'),
      include=task_modules
  )

  # Optional configuration, see the application user guide.
  app.conf.update(
      CELERY_TASK_RESULT_EXPIRES=cc.getint('celery.expires')
  )
  return app


class TaskNotifier(object):
  """
  utility to encapsulate the notifier behavior using redis pub usb
  """

  def __init__(self):
    from phovea_server.plugin import lookup
    from phovea_server.config import view as config_view
    # call lookup to enforce registry initialization which triggers configuration initialization
    lookup('test')
    cc = config_view('phovea_processing_queue.celery')
    self._db = redis.Redis(host=cc.host, port=cc.port, db=cc.db)
    self._channel_name = 'phovea_processing_channel'

  def listen(self):
    """
    listens to tasks changes
    :return: a generator for notifications
    """
    import json
    p = self._db.pubsub(ignore_subscribe_messages=True)
    p.subscribe(self._channel_name)
    for msg in p.listen():
      if msg['type'] == 'message':
        yield json.loads(msg['data'])

  def send(self, task_id, task_name, task_status):
    """
    send a task change
    :param task_id:  task id
    :param task_name:  task name
    :param task_status: the status (success, failure)
    :return:
    """
    # send a message using redis
    # print('send', task_id, task_name, task_status)
    self._db.publish(self._channel_name,
                     '{{ "task_id": "{}", "task_name": "{}", "task_status": "{}" }}'.format(task_id, task_name,
                                                                                            task_status))


class BaseTask(Task):
  """
  base class for processing tasks that report automatically when they are done using redis
  """
  abstract = True

  def on_success(self, retval, task_id, args, kwargs):
    notifier.send(task_id, self.name, 'success')

  def on_failure(self, exc, task_id, args, kwargs, einfo):
    notifier.send(task_id, self.name, 'failure')


# create a notifier instance
notifier = TaskNotifier()

# create celery
app = _create_celery()

# use my base class all the time
task = functools.partial(app.task, base=BaseTask)

# use common name
getLogger = get_task_logger


def get_result(task_id):
  """
  wrapper around AsyncResult to avoid importing
  :param task_id:
  :return:
  """
  return AsyncResult(task_id, app=app)


# just expose the needed stuff
__all__ = ['task', 'app', 'BaseTask', 'notifier', 'getLogger', 'get_result']
