#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, print_function

import pyquery

from robobrowser import RoboBrowser

__author__ = 'ytyng'
__version__ = '0.1'
__license__ = 'BSD'


class RoboBrowserQuery(RoboBrowser):
    @property
    def query(self):
        if not hasattr(self.state, 'pyquery'):
            self.state.pyquery = pyquery.PyQuery(
                self.state.response.content)

        return self.state.pyquery
