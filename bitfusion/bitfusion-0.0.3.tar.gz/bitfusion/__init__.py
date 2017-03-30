from requests.auth import AuthBase

from bitfusion import api
from bitfusion.lib import http_api

class BFApi():
  # Set the API data controllers
  Gpu = api.Gpu
  Node = api.Node
  Volume = api.Volume
  Workspace = api.Workspace

  def __init__(self, host='http://localhost:5000',
               auth=None, cookie=None, username=None, password=None):

    # Configure HTTP endpoint
    self.host = host
    self._set_http_endpoint()

    # Configure auth
    self.auth = auth
    self.username = username
    self.password = password
    self.cookie = cookie

    if self.auth:
      self.set_auth()
    elif self.cookie:
      self.set_cookie()
    elif self.username and self.password:
      self.login()


  def _set_http_endpoint(self):
    http_api.HTTP_HOST = self.host


  def login(self, username=None, password=None):
    payload = {
      'email': username or self.username,
      'password': password or self.password
    }

    http_api.API.post('/auth/login', payload)


  def set_auth(self, auth=None):
    http_api.AUTH_HANDLER = auth or self.auth


  def set_cookie(self, cookie=None):
    http_api.API.cookies.set('bf.sid', cookie or self.cookie)
