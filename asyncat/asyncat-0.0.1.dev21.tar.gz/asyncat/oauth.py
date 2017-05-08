#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""This module provides OAuth authentication."""
from __future__ import print_function, division, unicode_literals


class OAuth(object):        # pylint: disable=R0903
    """Github OAuth helper to get OAuth url."""
    def __init__(self, client, client_id, client_secret):
        """Initialize

        :type client: `~asyncat.client.AsyncGithubClient`
        """
        self._client = client
        self.__client_id = client_id
        self.__client_secret = client_secret

    def get_url(self, redirect_uri, scopes, state):
        """ Get OAuth url to redirect users to request Github access

        :pram redirect_uri:  Github redirects back URL
        :param scopes: scopes
        :type scopes: list of :class:`~asyncat.enumeration.Scope`
        :param state: an unguessable random string.
        """
        return self._client.get_url("/login/oauth/authorize", [
            ("client_id", self.__client_id),
            ("redirect_uri", redirect_uri),
            ("scope", " ".join([x.value for x in scopes])),
            ("state", state),
        ], host="https://github.com")
