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
from corenetwork.corosync_mixin import CorosyncMixin
from corenetwork.command_line_mixin import CommandLineMixin
from corenetwork.utils import config
from corenetwork.utils.logger import log


class Driver(CorosyncMixin, NetworkMixin, ApiMixin, OsMixin, CommandLineMixin, DriverInterface):
    agents = []

    def _suspend_vms(self):
        log("suspend_vms: not implemented", tags=('system', 'error'))


    def configure_node(self):
        """
        This method is called at node, by cc-node, when it is being configured.
        Use cc-node configure to start this action. It should be called only
        after cluster configuration is changed.
        """
        super(Driver, self).configure_node()
        self._check_i_am_root()
        self._register_node()
        self._configure_node_user()

    def startup_node(self):
        """
        This method is called when node is started, by cc-node
        """
        self._corosync_configure(core=False)
        self._check_updates('corenode', config.get('node', 'INSTALLATION_ID', 'none'))
        self._update_state('ok', 'Node service started')
        super(Driver, self).startup_node()


    def shutdown_node(self):
        """
        This method is called at node by cc-node, when it is going to shutdown.
        """
        self._suspend_vms()
        super(Driver, self).shutdown_node()

