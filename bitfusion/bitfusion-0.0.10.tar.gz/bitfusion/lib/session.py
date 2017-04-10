import sys
import os

import requests

from bitfusion import errors

class ApiSession(requests.Session):
  def __init__(self, host_url, auth_handler, timeout, *args, **kwargs):
    super(ApiSession, self).__init__(*args, **kwargs)

    self.host = host_url
    self.auth = auth_handler
    self.timeout = timeout


  def get(self, suffix):
    res = super(ApiSession, self).get(self._build_url(suffix),
                                      timeout=self.timeout,
                                      auth=self.auth)
    return self._handle_response(res)


  def post(self, suffix, data=None):
    res = super(ApiSession, self).post(self._build_url(suffix),
                                       json=data,
                                       timeout=self.timeout,
                                       auth=self.auth)
    return self._handle_response(res)


  def put(self, suffix, data):
    res = super(ApiSession, self).put(self._build_url(suffix),
                                      json=data,
                                      timeout=self.timeout,
                                      auth=self.auth)
    return self._handle_response(res)


  def delete(self, suffix):
    res = super(ApiSession, self).delete(self._build_url(suffix),
                                         timeout=self.timeout,
                                         auth=self.auth)
    return self._handle_response(res)


  def _build_url(self, suffix):
      return self.host + os.path.join(suffix)


  def _handle_response(self, res):
    try:
      res.raise_for_status()
    except requests.exceptions.HTTPError as e:
      self._handle_request_error(res)

    try:
      return res.json()
    except:
      raise Exception('Non-JSON response: {}'.format(res.text))


  def _handle_request_error(self, res):
    if res.status_code == 401:
      raise errors.AuthError()
    elif res.status_code == 403:
      raise errors.PermissionError()
    elif res.status_code >= 400 and res.status_code < 500:
      raise errors.ClientError(res.text)
    elif res.status_code >= 500:
      raise errors.APIError(res.text)
    else:
      raise Exception('Unknown error occured. Status: {} Response: {}'.format(res.status_code,
                                                                             res.text))
