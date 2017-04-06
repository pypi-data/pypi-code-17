#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'


class ObjectManager(object):
    def __init__(self):
        self.server_url = None
        self.access_key_id = ""
        self.access_key_secret = ""

    def set_server_url(self, server_url):
        self.server_url = server_url

    def set_access_key_id(self, access_key_id):
        self.access_key_id = access_key_id

    def set_access_key_secret(self, access_key_secret):
        self.access_key_secret = access_key_secret
