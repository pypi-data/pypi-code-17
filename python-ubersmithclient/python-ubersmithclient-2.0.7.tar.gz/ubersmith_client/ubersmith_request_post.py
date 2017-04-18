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

import requests

from ubersmith_client import _http_utils
from ubersmith_client.ubersmith_request import UbersmithRequest


class UbersmithRequestPost(UbersmithRequest):
    def __call__(self, **kwargs):
        self._build_request_params(kwargs)
        params = _http_utils.form_encode(kwargs)

        response = self._process_request(method=requests.post,
                                         url=self.url,
                                         auth=(self.user, self.password),
                                         timeout=self.timeout,
                                         headers={'user-agent': 'python-ubersmithclient'},
                                         data=params)

        return UbersmithRequest.process_ubersmith_response(response)
