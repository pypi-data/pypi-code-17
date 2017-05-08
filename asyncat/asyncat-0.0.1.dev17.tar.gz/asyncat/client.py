#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""This module provides AsyncGithubClient."""
from __future__ import print_function, division, unicode_literals


import json

from tornado import gen
from tornado import httpclient

try:
    from urllib import urlencode            # pragma: no cover
except ImportError:
    from urllib.parse import urlencode      # pragma: no cover


class GithubError(Exception):
    """Exception of GithubAsyncClient"""
    def __init__(self, response=None):
        """Initialize"""
        if response:
            msg = self._parse_response(response)
            self.status_code = response.code
        else:
            msg = None
            self.status_code = None

        super(GithubError, self).__init__(msg)

    @staticmethod
    def _parse_response(resp):
        """ Parse message from response """
        msg = "\n".join([
            "Status: {}".format(resp.code),
            "Body: {}".format(resp.body.decode("utf8"))
        ])
        return msg.encode("utf8")


class AsyncGithubClient(object):
    """ Asynchronous Github client """

    def __init__(self, access_token=None):
        self.__access_token = access_token
        self._host = "https://api.github.com"
        self._httpclient = httpclient.AsyncHTTPClient()

    def get_url(self, path, query_params=None, host=None):
        """ Returns the complete url with ``path`` and ``query_params`` """

        if host is None:
            host = self._host

        if query_params is not None:
            path = "{}?{}".format(path.rstrip("?"),
                                  urlencode(query_params))

        return "{}{}".format(host, path)

    def set_access_token(self, access_token):
        """Set access token."""
        self.__access_token = access_token

    @gen.coroutine
    def request(self, path, params=None, **kwargs):
        """ Use ``params`` to request Github  """
        headers = kwargs.get("headers", {})

        headers.update({
            "Accept": "application/json",
            "User-Agent": "Asyncat-Library",
        })

        if self.__access_token is not None:
            headers.update({
                "Authorization": "token {}".format(self.__access_token)
            })
        kwargs["headers"] = headers

        host = kwargs.pop("host", None)

        if kwargs.get("method", "GET") == "GET":
            url = self.get_url(path, params, host=host)
        else:
            if params is not None:
                kwargs["body"] = json.dumps(params)
            url = self.get_url(path, host=host)

        try:
            resp = yield self._httpclient.fetch(url, **kwargs)
        except httpclient.HTTPError as e:
            raise GithubError(e.response)

        if resp.body:
            data = json.loads(resp.body)

            # Bind data to the response
            resp.data = data
        raise gen.Return(resp)
