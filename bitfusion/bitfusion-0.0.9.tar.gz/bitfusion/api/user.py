from bitfusion.api.base import BaseMixin

def UserFactory(api_session):
  ###########################################
  # BEGIN User Class
  ###########################################
  class User(BaseMixin):
    api = api_session
    base_url = '/users'


    def load(self, api_data):
      # Set the ID at the top level so BaseMixin.load can parse it
      api_data['id'] = api_data.get('user', {}).get('_id')
      super(User, self).load(api_data)
  ###########################################
  # END User Class
  ###########################################

  return User
