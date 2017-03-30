import os

from requests.auth import AuthBase

from bitfusion import api
from bitfusion.lib import http_api

class BFApi():
  # Set the API data controllers
  Gpu = api.Gpu
  Node = api.Node
  Volume = api.Volume
  Workspace = api.Workspace

  def __init__(self, host='http://localhost:5000', api_base_url='/api',
               auth=None, cookie=None, username=None, password=None):

    if api_base_url:
      self.set_api_base_url(api_base_url)

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


  def set_api_base_url(self, base_path):
    self.Node.set_base_url(os.path.join(base_path, self.Node.base_url))
    self.Volume.set_base_url(os.path.join(base_path, self.Volume.base_url))
    self.Workspace.set_base_url(os.path.join(base_path, self.Workspace.base_url))

  def set_auth(self, auth=None):
    http_api.AUTH_HANDLER = auth or self.auth


  def set_cookie(self, cookie=None):
    http_api.API.cookies.set('bf.sid', cookie or self.cookie)
