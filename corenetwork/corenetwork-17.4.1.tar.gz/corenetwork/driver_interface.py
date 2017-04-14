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

import importlib
from corenetwork.utils import config
from corenetwork.exceptions.config import *


class DriverInterface(object):
    '''
    This class delivers interface for any driver, which responsible for node, vm or core network setup
    '''
    def __init__(self):
        super(DriverInterface, self).__init__()


    def configure_node(self):
        """
        This method is called at node, by corenode, when it is being configured.
        Use "cc-node configure" to start this action. It should be called only
        after cluster configuration is changed.
        """
        pass

    def startup_node(self):
        """
        This method is called when node is started, by corenode start
        """
        pass

    def shutdown_node(self):
        """
        This method is called at node by corenode, when it is going to shutdown.
        """
        pass


    def configure_core(self):
        """
        This method is called at Core installation by "cc-manage agent", when core shall be configured.
        """
        pass


    def startup_core(self):
        """
        This method is called at Core installation, by "cc-manage agent". It starts all agents and manages
        all startup-related tasks.
        """
        pass


    def shutdown_core(self):
        """
        This method is called when Core goes to shutdown. It is called by "cc-manage agent"
        """
        pass


    def prepare_vm(self, vm_name):
        """
        This method is called by Libvirt hook, when VM is defined in Libvirt
        """
        pass


    def startup_vm(self, vm_name):
        """
        This method is called by Libvirt hook, when VM is is powered on
        """
        pass


    def release_vm(self, vm_name):
        """
        This method is called by Libvirt hook, when VM is powered off
        """
        pass


    def start_network(self, network_name):
        """
        This method is called when new network (exactly lease) is created in libvirt (at node)
        """
        pass


    def stop_network(self, network_name):
        """
        This method is called when new network (exactly lease) is destroyed in libvirt (at node)
        """
        pass


    def info_node(self, action, id=None):
        """
        Manage or get information about nodes
        """
        pass


    def info_vm(self, action, id=None):
        """
        Manage vm objects in cluster
        """
        pass


    def info_task(self, action, id=None):
        """
        Manage tasks
        """
        pass


    def info_agent(self, action, id=None):
        """
        Manage agents
        """
        pass


    def info_subnet(self, action, id=None):
        """
        Manage subnets
        """
        pass


    def info_network_pool(self, action, id=None):
        """
        Manage subnets
        """
        pass


    def info_storage(self, action, id=None):
        """
        Manage storages
        """
        pass


    def info_api(self, action, id=None):
        """
        Manage agents
        """
        pass

    def info_image(self, action, id):
        """
        Manage images at cloud storage
        """
        pass

    @staticmethod
    def _get_driver(driver_name):
        driver_module = None
        try:
            apps = config.get('core', 'APPS')
        except:
            apps = config.get('node', 'APPS')

        for app_name in apps:
            app = importlib.import_module(app_name).MODULE
            if 'drivers' in app and driver_name in app['drivers']:
                driver_module = app['drivers'][driver_name]

        if driver_module is not None:
            driver = importlib.import_module(driver_module)
            return driver.Driver()
        else:
            raise ConfigVariableNotFound('DRIVER:' + driver_name)


    @staticmethod
    def get_network_routed_driver():
        return DriverInterface._get_driver('NETWORK_ROUTED_DRIVER')


    @staticmethod
    def get_network_isolated_driver():
        return DriverInterface._get_driver('NETWORK_ISOLATED_DRIVER')


    @staticmethod
    def get_node_driver():
        return DriverInterface._get_driver('NODE_DRIVER')


    @staticmethod
    def get_core_driver():
        return DriverInterface._get_driver('CORE_DRIVER')


    @staticmethod
    def get_vm_driver():
        return DriverInterface._get_driver('VM_DRIVER')


    @staticmethod
    def get_all_drivers():
        return [DriverInterface.get_network_isolated_driver(),
                DriverInterface.get_network_routed_driver(),
                DriverInterface.get_node_driver(),
                DriverInterface.get_core_driver(),
                DriverInterface.get_vm_driver()]
