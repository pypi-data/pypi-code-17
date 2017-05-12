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

from application.dao.database import Database


class CurrentDao(object):

    def __init__(self, data_path):
        self.data_path = data_path + 'current/'

    def load(self):
        return self._read_file()

    def save(self, bank_index, pedalboard_index):
        json = {
            "bank": bank_index,
            "pedalboard": pedalboard_index
        }

        Database.save(self._url(), json)

    def _read_file(self):
        return Database.read(self._url())

    def _url(self):
        return self.data_path + "current.json"
