import os

from dateutil import parser as dt_parser

from bitfusion.api.base import BaseMixin, CreatableMixin
from bitfusion.lib import time

"""
EXAMPLE API MODEL:
{
  "status": "new",
  "deletedAt": null,
  "deleted": false,
  "runEnv": "tensorflow",
  "cmd": [
    "python test.py"
  ],
  "createdAt": "2017-04-28T16:04:48.584Z",
  "groupId": "59022ab6c9451b00118b8b44",
  "project": {
    "_id": "590279b5156ceb0056d07b36",
    "name": "test",
    "id": "590279b5156ceb0056d07b36"
  },
  "ready": false,
  "__v": 0,
  "stoppedAt": null,
  "createdBy": "59022ab6c9451b00118b8b43",
  "updatedAt": "2017-04-28T16:04:48.594Z",
  "duration": 0,
  "startedAt": null,
  "_id": "5903682067dad8002092656a",
  "data": {
    "in": [],
    "out": {
      "status": "ready",
      "name": "output",
      "deleted": false,
      "fileName": "out.txt",
      "__v": 0,
      "updatedAt": "2017-04-28T16:04:48.589Z",
      "deletedAt": null,
      "path": {
        "remote": "59022ab6c9451b00118b8b45/59022ab6c9451b00118b8b44/projects/undefined/jobs/5903682067dad8002092656a/out"
      },
      "_id": "5903682067dad8002092656b",
      "id": "5903682067dad8002092656b",
      "createdAt": "2017-04-28T16:04:48.588Z"
    }
  },
  "id": "5903682067dad8002092656a",
  "resources": [],
  "accountId": "59022ab6c9451b00118b8b45"
}
"""

def JobFactory(api_session):
  ###########################################
  # BEGIN Job Class
  ###########################################
  class Job(BaseMixin, CreatableMixin):
    api = api_session
    base_url = '/api/jobs'

    def __str__(self):
      output = 'Job {id}'

      if self.data.get('stoppedAt'):
        stopped_time = time.str_start_to_str_runtime(self.data.get('stoppedAt'))
        output = output + ' - stopped {stopped} ago'.format(stopped=stopped_time)
      elif self.data.get('startedAt'):
        runtime = time.str_start_to_str_runtime(self.data.get('startedAt'))
        output = output + ' - started {runtime} ago'.format(runtime=runtime)
      elif self.data.get('createdAt'):
        created_time = time.str_start_to_str_runtime(self.data.get('createdAt'))
        output = output + ' - created {created} ago'.format(created=created_time)

      output = output.format(id=self.data.get('id'))
      return output


    def logs(self):
      return self.api.get(os.path.join(self.base_url, self.id, 'logs'))


    @classmethod
    def create(cls, project, code_id, group, env, command):
      if isinstance(command, str):
        command = command.split(' ')
      elif not isinstance(command, list):
        raise Exception('command must be a string or a list')

      payload = {
        'groupId': group,
        'project': project,
        'cmd': command,
        'runEnv': env,
        'codeset': code_id
      }

      return super(Job, cls).create(**payload)
  ###########################################
  # END Job Class
  ###########################################

  return Job
