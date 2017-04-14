"""
Copyright (C) 2014-2017 cloudover.io ltd.
This file is part of the CloudOver.org project

Licensee holding a valid commercial license for this software may
use it in accordance with the terms of the license agreement
between cloudover.io ltd. and the licensee.

Alternatively you may use this software under following terms of
GNU Affero GPL v3 license:

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version. For details contact
with the cloudover.io company: https://cloudover.io/


This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.


You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from corenetwork.network_mixin import NetworkMixin
from corenetwork.os_mixin import OsMixin
from corenetwork.api_mixin import ApiMixin
from corenetwork.hook_interface import HookInterface
from corenetwork.utils import config
import random
import hashlib


class Hook(NetworkMixin, OsMixin, ApiMixin, HookInterface):
    vm_name = ''

    def start(self):
        super(Hook, self).start()
        auth_seed = hashlib.sha256(str(random.random())).hexdigest()
        self._request('ci/vm/update_state/', {'auth_hash': self._calc_hash(config.get('node', 'AUTH_TOKEN'), auth_seed),
                                              'auth_seed': auth_seed,
                                              'vm_name': self.vm_name,
                                              'state': 'running'})


    def finish(self):
        super(Hook, self).finish()
        auth_seed = hashlib.sha256(str(random.random())).hexdigest()
        self._request('ci/vm/update_state/', {'auth_hash': self._calc_hash(config.get('node', 'AUTH_TOKEN'), auth_seed),
                                              'auth_seed': auth_seed,
                                              'vm_name': self.vm_name,
                                              'state': 'stopped'})
