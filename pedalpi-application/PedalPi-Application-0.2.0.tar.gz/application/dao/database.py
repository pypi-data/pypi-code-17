# Copyright 2017 SrMouraSilva
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

import json
import os
import asyncio


class Database(object):

    @staticmethod
    def read(url):
        with open(url) as data_file:
            return json.load(data_file)

    @staticmethod
    def save(url, data):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(Database._save(url, data))
        except AssertionError:
            Database._save(url, data)

    @staticmethod
    @asyncio.coroutine
    def _save(url, data):
        json_file = open(url, "w+")
        json_file.write(json.dumps(data))
        json_file.close()

    @staticmethod
    def delete(url):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(Database._delete(url))
        except AssertionError:
            Database._delete(url)

    @staticmethod
    @asyncio.coroutine
    def _delete(url):
        os.remove(url)
