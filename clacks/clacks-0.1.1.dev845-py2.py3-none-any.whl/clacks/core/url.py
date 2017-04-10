#!/usr/bin/env python3

""" Url parsing class that understands path encoded params."""


class Url():
    """Url wrapper class"""

    def __init__(self, url=None):
        self.path_params = []
        if url:
            self._url = url

    def set_path_param(self, param, value):
        """update url to containg given param, by adding or replacing it in the url"""
        pass
