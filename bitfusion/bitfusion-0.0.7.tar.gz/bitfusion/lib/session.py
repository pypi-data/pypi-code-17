import sys
import os

import requests


class ApiSession(requests.Session):
  def __init__(self, host_url, auth_handler, timeout, *args, **kwargs):
    self.host = host_url
    self.auth = auth_handler
    self.timeout = timeout

    super(ApiSession, self).__init__(*args, **kwargs)

  def get(self, suffix):
    try:
      res = super(ApiSession, self).get(self._build_url(suffix),
                                        timeout=self.timeout,
                                        auth=self.auth)
    except Exception as e:
      return self._handle_request_error(e)

    return self._handle_response(res)


  def post(self, suffix, data=None):
    try:
      res = super(ApiSession, self).post(self._build_url(suffix),
                                         json=data,
                                         timeout=self.timeout,
                                         auth=self.auth)
    except Exception as e:
      return self._handle_request_error(e)

    return self._handle_response(res)


  def put(self, suffix, data,):
    try:
      res = super(ApiSession, self).put(self._build_url(suffix),
                                        json=data,
                                        timeout=self.timeout,
                                        auth=self.auth)
    except Exception as e:
      return self._handle_request_error(e)

    return self._handle_response(res)


  def delete(self, suffix):
    try:
      res = super(ApiSession, self).delete(self._build_url(suffix),
                                           timeout=self.timeout,
                                           auth=self.auth)
    except Exception as e:
      return self._handle_request_error(e)

    return self._handle_response(res)

  def _build_url(self, suffix):
      return self.host + os.path.join(suffix)

  def _handle_response(self, res):
    try:
      res.raise_for_status()
    except requests.exceptions.HTTPError as e:
      self._handle_request_error(e)

    try:
      return res.json()
    except:
      raise Exception('Non-JSON response: {}'.format(res.text))


  def _handle_request_error(self, e):
    raise Exception({'errors': str(e)})
