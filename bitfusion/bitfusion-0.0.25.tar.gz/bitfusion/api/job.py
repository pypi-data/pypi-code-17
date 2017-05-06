import datetime
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

def get_resource_string(resources):
  if not resources:
    return ''

  tran_r_array = [_r.get('type', '') + '=' + str(_r.get('value')) for _r in resources]
  return ','.join(tran_r_array)


def JobFactory(api_session):
  ###########################################
  # BEGIN Job Class
  ###########################################
  class Job(BaseMixin, CreatableMixin):
    api = api_session
    base_url = '/api/jobs'

    def __str__(self):
      output = 'Job {id} - ' + self.get_state_string()
      output = output.format(id=self.data.get('id'))
      return output


    def get_state_string(self):
      if self.data.get('stoppedAt'):
        stopped_time = time.str_start_to_str_runtime(self.data.get('stoppedAt'))
        return 'Stopped {stopped} ago'.format(stopped=stopped_time)
      elif self.data.get('startedAt'):
        runtime = time.str_start_to_str_runtime(self.data.get('startedAt'))
        return 'Started {runtime} ago'.format(runtime=runtime)
      elif self.data.get('createdAt'):
        created_time = time.str_start_to_str_runtime(self.data.get('createdAt'))
        return 'Created {created} ago'.format(created=created_time)


    def logs(self):
      return self.api.get(os.path.join(self.base_url, self.id, 'logs'))


    def get_table_row(self):
      resource_str = get_resource_string(self.data.get('resources'))
      durstr = time.get_duration_string(self.data.get('startedAt'), self.data.get('stoppedAt'))

      return [
        self.data.get('id'),
        self.data.get('project', {}).get('name'),
        time.str_start_to_str_runtime(self.data.get('createdAt')) + ' ago',
        self.data.get('status'),
        durstr,
        resource_str
      ]


    @staticmethod
    def get_table_headers():
      return ['ID', 'Project', 'Created', 'Status', 'Duration', 'Resources']


    @classmethod
    def create(cls, project, code_id, group, env, data_ids, resources, command):
      if isinstance(command, str):
        command = command.split(' ')
      elif not isinstance(command, list):
        raise Exception('command must be a string or a list')

      payload = {
        'groupId': group,
        'project': project,
        'cmd': command,
        'runEnv': env,
        'codeset': code_id,
        'dataset': data_ids,
        'resources': resources,
      }

      return super(Job, cls).create(**payload)
  ###########################################
  # END Job Class
  ###########################################

  return Job
