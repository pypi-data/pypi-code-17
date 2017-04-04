from bitfusion.api.base import BaseMixin

def GpuFactory(api_session):
  ###########################################
  # BEGIN Gpu Class
  ###########################################
  class Gpu(BaseMixin):
    api = api_session

    def __str__(self):
      output = 'GPU {id} - {type} - {mem} MB Memory - {state}'
      output = output.format(id=self.data['id'],
                             type=self.data['type'],
                             mem=self.data.get('memory', '???'),
                             state=self.data['state'])

      return output
  ###########################################
  # END Gpu Class
  ###########################################

  return Gpu
