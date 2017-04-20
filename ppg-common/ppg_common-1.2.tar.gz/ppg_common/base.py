import json

import requests
from errors.blossom import BlossomHTTPErrors, BlossomHTTPError
from errors.buttercup import ButterCupHTTPErrors, ButterCupHTTPException

from ppg_common.errors.bubbles import BubblesHttpErrors, BubblesHttpError


def handle_response(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        body = None
        if len(response.content):
            body = response.json()
        if 400 <= response.status_code < 500 and body and \
                body.get('message') and body.get('code'):
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

    @handle_response
    def get(self, path, query="", headers=None):
        if headers is None:
            headers = {}
        url = self.create_url(path, query)
        headers.update(self.base_headers)
        return requests.get(url, headers=headers)

    @handle_response
    def post(self, path, body, query="", headers=None):
        if headers is None:
            headers = {}
        url = self.create_url(path, query)
        headers.update(self.base_headers)
        return requests.post(url, headers=headers,
                             data=json.dumps(body))

    @handle_response
    def put(self, path, body, query="", headers=None):
        if headers is None:
            headers = {}
        url = self.create_url(path, query)
        headers.update(self.base_headers)
        return requests.put(url, headers=headers,
                            data=json.dumps(body))

    @handle_response
    def patch(self, path, body, query="", headers=None):
        if headers is None:
            headers = {}
        url = self.create_url(path, query)
        headers.update(self.base_headers)
        return requests.patch(url, headers=headers,
                              data=json.dumps(body))

    @handle_response
    def delete(self, path, query="", headers=None):
        if headers is None:
            headers = {}
        url = self.create_url(path, query)
        headers.update(self.base_headers)
        return requests.delete(url, headers=headers)
