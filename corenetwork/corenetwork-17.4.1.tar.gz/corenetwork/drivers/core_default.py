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
from django.db.models import Q

from corenetwork.driver_interface import DriverInterface
from corenetwork.network_mixin import NetworkMixin
from corenetwork.os_mixin import OsMixin
from corenetwork.api_mixin import ApiMixin
from corenetwork.corosync_mixin import CorosyncMixin
from corenetwork.command_line_mixin import CommandLineMixin
from corenetwork.webserver_mixin import WebServerMixin
from corenetwork.utils import config
from corenetwork.utils.logger import log


class Driver(CommandLineMixin, WebServerMixin, CorosyncMixin, NetworkMixin, ApiMixin, OsMixin, DriverInterface):
    agents = []

    def _cleanup_queues(self):
        from corecluster.cache import Cache

        if config.get('agent', 'CLEANUP_QUEUES_ON_START', True):
            for k in Cache.keys():
                print('Deleting %s' % k)
                Cache.delete(k)


    def _mount_storages(self):
        from corecluster.cache.task import Task
        from corecluster.models.core.node import Node
        from corecluster.models.core.storage import Storage

        if config.get('agent', 'MOUNT_NODES'):
            # Lock all nodes
            for node in Node.objects.filter(state='ok'):
                node.state = 'offline'
                node.save()


            # Mount all storages at core
            for s in Storage.objects.filter(Q(state='locked') | Q(state='ok')).all():
                s.state = 'locked'
                s.save()

                mnt = Task()
                mnt.type = 'storage'
                mnt.action = 'mount'
                mnt.append_to([s])


            # Mpunt all storages on all nodes
            for node in Node.objects.filter(Q(state='ok') | Q(state='offline')):
                node.start(Storage.objects.filter(Q(state='locked') | Q(state='ok')).all())


    def _create_networks(self):
        from corecluster.models.core import Subnet

        for network in Subnet.objects.filter(network_pool__mode='isolated').all():
            network.prepare()


    def _start_agents(self):
        """
        Start all agents as child processes
        """
        for app_name in config.get('core', 'APPS'):
            app = importlib.import_module(app_name).MODULE
            if 'agents' in app:
                for agent in app['agents']:
                    for i in xrange(agent['count']):
                        log(msg="start_agents: starting agent %s" % agent['type'], tags=('system', 'info', 'agent'))
                        print("start_agents: starting agent %s" % agent['type'])
                        agent_module = importlib.import_module(agent['module'])
                        thread = agent_module.AgentThread()
                        thread.start()
                        self.agents.append(thread)


    def _stop_agents(self):
        from corecluster.models.core import Agent

        for agent in self.agents:
            log(msg="stop_agents: suspending agent %s" % agent, tags=('system', 'info', 'agent'))
            agent_obj = Agent.objects.get(pk=agent.agent.id)
            agent_obj.set_state('stopping')
            agent_obj.save()

        for agent in self.agents:
            log(msg="stop_agents: stopping agent %s" % agent, tags=('system', 'info', 'agent'))
            agent.join()
            log(msg="stop_agents: done", tags=('system', 'info', 'agent'))
        log(msg="stop_agents: all agents stopped", tags=('system', 'info', 'agent'))


    def _suspend_vms(self):
        log(msg="suspend_vms: not implemented", tags=('system', 'info', 'vm'))

    def configure_core(self):
        """
        This method is called at Core installation by "cc-manage agent", when core shall be configured.
        """
        super(Driver, self).configure_core()
        self._configure_core_user()
        self._configure_webserver()
        self._corosync_keygen()
        self._corosync_configure(core=True)

    def startup_core(self):
        """
        This method is called at Core installation, by "cc-manage agent". It starts all agents and manages
        all startup-related tasks. First action of this methid is to change to cloudover user. If you need
        to inherit it in your driver and perform some actions as root - call super(...) after root's actions.
        """
        super(Driver, self).startup_core()
        self._cleanup_queues()
        self._become_cloudover()
        self._initialize_iptables()
        self._mount_storages()
        self._create_networks()
        self._start_agents()
        self._check_updates('corecluster', config.get('core', 'INSTALLATION_ID', 'none'))


    def shutdown_core(self):
        """
        This method is called when Core goes to shutdown. It is called by "cc-manage agent"
        """
        self._stop_agents()
        self._cleanup_iptables()
        super(Driver, self).shutdown_core()
