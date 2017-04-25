import os

class BaseMixin(object):
  def __init__(self, **kwargs):
    self.load(kwargs)


  def load(self, api_data):
    self.id = api_data.get('id')
    self.data = api_data


  def reload(self):
    if not self.id:
      raise Exception('Cannot reload an object that has no ID')

    self.load(self.get_data_by_id(self.id))


  def delete(self):
    return self.api.delete(os.path.join(self.base_url, str(self.id)))


  @classmethod
  def set_base_url(cls, base_url):
    cls.base_url = base_url


  @classmethod
  def get(cls, data_id):
    return cls(**cls.get_data_by_id(data_id))


  @classmethod
  def get_all(cls):
    raw_data = cls.api.get(cls.base_url)
    instance_list = []

    for d in raw_data:
      instance_list.append(cls(**d))

    return instance_list


  @classmethod
  def get_data_by_id(cls, data_id):
    return cls.api.get(os.path.join(cls.base_url, str(data_id)))


class CreatableMixin(object):
  @classmethod
  def create(cls, **kwargs):
    return cls(**cls.api.post(cls.base_url, kwargs))

class UpdateableMixin(object):
  def update(self, **kwargs):
    if not self.id:
      raise Exception('Cannot update without an ID')

    self.load(self.api.put(os.path.join(self.base_url, str(self.id)), kwargs))

class HealthMixin(object):
  def set_health(self, health_status, health_message):
    self.update(state=health_status, health_message=health_message)
