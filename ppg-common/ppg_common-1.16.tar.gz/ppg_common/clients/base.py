import json
import requests
from ppg_common.errors import (
    ButterCupHTTPErrors, ButterCupHTTPException, BlossomHTTPError,
    BlossomHTTPErrors, BubblesHttpError, BubblesHttpErrors,
    PpgHttpErrors, PpgHTTPError
)


def handle_response(func):
    def wrapper(self, *args, **kwargs):
        if kwargs.get('headers') is None:
            kwargs['headers'] = {}
        kwargs['headers'].update(self.base_headers)
        try:
            status_response = self.get_status()
        except:
            raise PpgHTTPError(PpgHttpErrors.INACTIVE)
        response = func(self, *args, **kwargs)
        body = None
        if len(response.content):
            body = response.json()
        if 400 <= response.status_code < 500 and body and body.get(
                'message') and body.get('code'):
            if 100 <= body.get('code') < 200:
                raise ButterCupHTTPException(
                    ButterCupHTTPErrors.error_map[body.get('code')])
            if 200 <= body.get('code') < 300:
                raise BlossomHTTPError(
                    BlossomHTTPErrors.error_map[body.get('code')])
            if 300 <= body.get('code') < 400:
                raise BubblesHttpError(
                    BubblesHttpErrors.error_map[body.get('code')])
        return body

    return wrapper


class BaseClient(object):
    def __init__(self, host, port, ssl=False, session=None):
        if ssl:
            self.base_url = "https://{}:{}".format(host, port)
        else:
            self.base_url = "http://{}:{}".format(host, port)

        self.base_headers = {
            'Accept': 'application/json', 'Content-Type': 'application/json'
        }
        if session is not None:
            self.base_headers.update({'x-session': session})

    def create_url(self, path, query=""):
        return "{}{}?{}".format(self.base_url, path, query)

    def change_session(self, session_id):
        self.base_headers.update({'x-session': session_id})

    def get_status(self):
        url = self.create_url('/v1/status')
        return requests.get(url)

    @handle_response
    def get(self, path, query="", headers=None):
        url = self.create_url(path, query)
        return requests.get(url, headers=headers)

    @handle_response
    def post(self, path, body, query="", headers=None):
        url = self.create_url(path, query)
        return requests.post(url, headers=headers,
                             data=json.dumps(body))

    @handle_response
    def put(self, path, body, query="", headers=None):
        url = self.create_url(path, query)
        return requests.put(url, headers=headers,
                            data=json.dumps(body))

    @handle_response
    def patch(self, path, body, query="", headers=None):
        url = self.create_url(path, query)
        return requests.patch(url, headers=headers,
                              data=json.dumps(body))

    @handle_response
    def delete(self, path, query="", headers=None):
        url = self.create_url(path, query)
        return requests.delete(url, headers=headers)
