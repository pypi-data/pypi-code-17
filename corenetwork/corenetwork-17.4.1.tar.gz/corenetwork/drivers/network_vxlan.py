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

import random

from corenetwork.utils import system
from corenetwork.network_mixin import NetworkMixin
from corenetwork.os_mixin import OsMixin
from corenetwork.api_mixin import ApiMixin
from corenetwork.driver_interface import DriverInterface

class Driver(NetworkMixin, OsMixin, ApiMixin, DriverInterface):
    def start_node(self):
        system.call('modprobe vxlan', shell=True)
        super(Driver, self).start_node()


    def start_core(self):
        system.call('modprobe vxlan', shell=True)
        super(Driver, self).start_core()
