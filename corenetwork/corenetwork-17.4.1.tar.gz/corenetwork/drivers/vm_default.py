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

from corenetwork.driver_interface import DriverInterface
from corenetwork.network_mixin import NetworkMixin
from corenetwork.os_mixin import OsMixin
from corenetwork.api_mixin import ApiMixin
from corenetwork.hook_interface import HookInterface


class Driver(NetworkMixin, ApiMixin, OsMixin, DriverInterface):
    def prepare_vm(self, vm_name):
        """
        This method is called by Libvirt hook, when VM is defined in Libvirt
        """
        super(Driver, self).prepare_vm(vm_name)
        hooks = HookInterface.get_hooks('vm.prepared')
        for hook in hooks:
            hook.vm_name = vm_name
            if hasattr(hook, 'prepare'):
                hook.prepare()


    def startup_vm(self, vm_name):
        """
        This method is called by Libvirt hook, when VM is is powered on
        """
        super(Driver, self).prepare_vm(vm_name)
        hooks = HookInterface.get_hooks('vm.started')
        for hook in hooks:
            hook.vm_name = vm_name
            if hasattr(hook, 'start'):
                hook.start()


    def release_vm(self, vm_name):
        """
        This method is called by Libvirt hook, when VM is powered off
        """
        super(Driver, self).prepare_vm(vm_name)
        hooks = HookInterface.get_hooks('vm.stopped')
        for hook in hooks:
            hook.vm_name = vm_name
            if hasattr(hook, 'finish'):
                hook.finish()


    def start_network(self, network_name):
        """
        This method is called when new network is created in libvirt
        """
        super(Driver, self).start_network(network_name)
        hooks = HookInterface.get_hooks('network.started')
        for hook in hooks:
            hook.network_name = network_name
            hook.start()


    def stop_network(self, network_name):
        """
        This method is called when new network is destroyed in libvirt
        """
        super(Driver, self).stop_network(network_name)
        hooks = HookInterface.get_hooks('network.stopped')
        for hook in hooks:
            hook.network_name = network_name
            hook.finish()
