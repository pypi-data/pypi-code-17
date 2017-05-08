#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""This module provides the base class of all the test case."""
from __future__ import print_function, division, unicode_literals

import os

import dotenv

from tornado import testing

from asyncat.client import AsyncGithubClient

DOT_ENVPATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')

if os.path.exists(DOT_ENVPATH):
    dotenv.load_dotenv(DOT_ENVPATH)

os.environ["ASYNC_TEST_TIMEOUT"] = "20"


class AsyncatTestCase(testing.AsyncTestCase):
    """Base class of test cases."""
    def setUp(self):
        super(AsyncatTestCase, self).setUp()
        token = os.environ.get("ASYNCAT_TOKEN")
        self.client = AsyncGithubClient(token)
