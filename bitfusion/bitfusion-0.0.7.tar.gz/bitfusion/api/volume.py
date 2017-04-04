from bitfusion.api.base import BaseMixin, CreatableMixin, UpdateableMixin

def VolumeFactory(api_session):
  class Volume(BaseMixin, CreatableMixin, UpdateableMixin):
  ###########################################
  # BEGIN Volume Class
  ###########################################
    api = api_session
    base_url = '/volume'

    def __str__(self):
      output = '\nVolume {id} - {name}\nHost: {host_path}\nContainer: {container_path}'
      output = output.format(id=self.data['id'],
                             name=self.data['name'],
                             host_path=self.data['host_path'],
                             container_path=self.data['container_path'])

      return output + '\n'
  ###########################################
  # END Volume Class
  ###########################################

  return Volume
