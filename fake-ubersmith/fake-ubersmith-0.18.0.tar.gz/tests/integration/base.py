# Copyright 2017 Internap.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import subprocess
import unittest

import requests
import ubersmith_client
from requests import RequestException
from retry.api import retry_call

logger = logging.getLogger()


class Base(unittest.TestCase):

    ub_client = None
    host = '127.0.0.1'
    port = 9131
    endpoint = 'http://{}:{}'.format(host, port)

    @classmethod
    def setUpClass(cls):
        cls._start_app_locally()
        cls.ub_client = ubersmith_client.api.init(
            url="{}/api/2.0/".format(cls.endpoint),
            user='username',
            password='password'
        )

    @classmethod
    def _set_new_endpoint(cls):
        cls.endpoint = 'http://{}:{}'.format(cls.host, cls.port)

    @classmethod
    def _start_app_locally(cls):
        subprocess.Popen(["fake-ubersmith"])
        retry_call(
            requests.get,
            fargs=["{}/status".format(cls.endpoint)],
            exceptions=RequestException,
            delay=1
        )

    @classmethod
    def tearDownClass(cls):
        requests.get("{}/__shutdown".format(cls.endpoint))
