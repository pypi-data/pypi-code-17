from bitfusion.api.base import BaseMixin, CreatableMixin, UpdateableMixin, HealthMixin

def UserFactory(api_session):
  class User(BaseMixin, CreatableMixin, UpdateableMixin):
