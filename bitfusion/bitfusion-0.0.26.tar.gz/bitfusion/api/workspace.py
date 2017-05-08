import os

from bitfusion.api.base import BaseMixin, CreatableMixin, UpdateableMixin, HealthMixin
from bitfusion.lib import time

def WorkspaceFactory(api_session, host, Gpu):
  ###########################################
  # BEGIN Workspace Class
  ###########################################
  class Workspace(BaseMixin, CreatableMixin, UpdateableMixin, HealthMixin):
    api = api_session
    base_url = '/api/workspace'

    def __str__(self):
      output = '\nWorkspace {id} - {name} - Active for {running} - {type}\n * {url}'

      url = host + self.data.get('url', '')

      if self.data.get('start_date'):
        running = time.str_start_to_str_runtime(self.data['start_date'])
      else:
        running = 'unknown'

      output = output.format(id=self.data.get('id'),
                             name=self.data.get('name', '(unnamed)'),
                             running=running,
                             type=self.data.get('type'),
                             url=url)

      for g in self.data.get('gpus', []):
        gpu = Gpu(**g)
        output += '\n\t' + str(gpu)

      return output + '\n'


    @classmethod
    def image_metadata(cls, image_type):
      images = cls.api.get(os.path.join(cls.base_url, 'type'))

      for _i in images:
        if _i['type'] == image_type:
          return _i

      return None


    @classmethod
    def images(cls):
      return cls.api.get(os.path.join(cls.base_url, 'type'))


    @classmethod
    def create(cls, ws_type, node_id, group, name=None, gpus=[], options=None):
      payload = {
        'type': ws_type,
        'node_id': node_id,
        'group': group,
        'name': name,
        'gpus': gpus,
        'options': options
      }

      return super(Workspace, cls).create(**payload)
  ###########################################
  # END Workspace Class
  ###########################################

  return Workspace
