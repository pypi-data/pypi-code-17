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

from glob import glob

from application.dao.database import Database
from pluginsmanager.util.persistence_decoder import PersistenceDecoder


class BankDao(object):

    def __init__(self, data_path):
        self.data_path = data_path + 'banks/'

    def banks(self, system_effect):
        persistence = PersistenceDecoder(system_effect)

        banks = []

        for file in glob(self.data_path + "*.json"):
            bank = persistence.read(Database.read(file))
            banks.append(bank)

        return sorted(banks, key=lambda b: b.index)

    def save(self, bank, index):
        bank.index = index
        Database.save(self._url(bank), bank.json)

    def delete(self, bank):
        Database.delete(self._url(bank))

    def _url(self, bank):
        return self.data_path + bank.original_name + ".json"
