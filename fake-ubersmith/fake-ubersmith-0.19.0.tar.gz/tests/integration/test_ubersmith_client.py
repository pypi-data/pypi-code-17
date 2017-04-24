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

from tests.integration.base import Base


class TestUbersmithClient(Base):
    def test_client_creation_works(self):
        client_id = self.ub_client.client.add(uber_login='username')

        result = self.ub_client.client.get(client_id=client_id)

        self.assertEqual(result, {'clientid': client_id, 'login': 'username'})
