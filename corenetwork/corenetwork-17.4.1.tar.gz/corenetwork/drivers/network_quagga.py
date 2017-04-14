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

import os
import random
import hashlib
import datetime
import django.conf
from django.template import Context, Template

from corenetwork.utils import system, config
from corenetwork.network_mixin import NetworkMixin
from corenetwork.os_mixin import OsMixin
from corenetwork.api_mixin import ApiMixin
from corenetwork.driver_interface import DriverInterface
from corenetwork.utils.logger import log


class Driver(NetworkMixin, OsMixin, ApiMixin, DriverInterface):
    ospf_config_path = '/etc/quagga/ospfd.conf'
    zebra_config_path = '/etc/quagga/zebra.conf'
    daemons_path = '/etc/quagga/daemons'


    def _render_template(self, path, interfaces):
        try:
            django.conf.settings.configure()
        except:
            pass
        t = Template(open(path).read(1024*1024*16))
        return t.render(Context({'interfaces': interfaces,
                                 'hostname': 'core',
                                 'password': config.get('network', 'QUAGGA_PASSWORD'),
                                 'ospf_token': config.get('network', 'OSPF_TOKEN'),
                                 'router_id': self._get_core_address()}))


    def _get_template(self, path,  interfaces):
        auth_seed = hashlib.sha256(str(random.random())).hexdigest()
        return self._request(path, {'auth_hash': self._calc_hash(config.get('node', 'AUTH_TOKEN'), auth_seed),
                                    'auth_seed': auth_seed,
                                    'interfaces': interfaces})


    def _setup_quagga(self, core=False):
        """
        Configure quagga daemon for dynamic routing
        """
        interfaces = self._get_interface_list()

        log(msg="setup_quagga: retreiving quagga templates", tags=('system', 'info'))

        if core:
            ospf_tmpl = self._render_template('/etc/corenetwork/drivers/quagga/ospfd.template.conf', interfaces)
            zebra_tmpl = self._render_template('/etc/corenetwork/drivers/quagga/zebra.template.conf', interfaces)
            daemons_tmpl = self._render_template('/etc/corenetwork/drivers/quagga/daemons.template.conf', interfaces)
        else:
            ospf_tmpl = self._get_template('ci/network_routed/get_ospfd_template/', interfaces)
            zebra_tmpl = self._get_template('ci/network_routed/get_zebra_template/', interfaces)
            daemons_tmpl = self._get_template('ci/network_routed/get_daemons_template/', interfaces)

        if config.get('network', 'CREATE_CONFIG_BACKUPS', False):
            log(msg='setup_quagga: creating configuration backup', tags=('system', 'info'))
            if os.path.exists(self.ospf_config_path):
                os.rename(self.ospf_config_path, self.ospf_config_path + '.%s' % str(datetime.datetime.now()))
            if os.path.exists(self.zebra_config_path):
                os.rename(self.zebra_config_path, self.zebra_config_path + '.%s' % str(datetime.datetime.now()))

        log(msg='setup_quagga: updating config', tags=('system', 'info'))
        ospf_conf = open(self.ospf_config_path, 'w')
        ospf_conf.write(ospf_tmpl)
        ospf_conf.close()

        zebra_conf = open(self.zebra_config_path, 'w')
        zebra_conf.write(zebra_tmpl)
        zebra_conf.close()

        daemons = open(self.daemons_path, 'w')
        daemons.write(daemons_tmpl)
        daemons.close()


    def _setup_cloudinit(self):
        core_ip = self._get_core_address()
        log(msg="setup_cloudinit: configuring cloudinit for address %s" % core_ip, tags=('system', 'info'))

        # Add redirection to Core
        system.call('ip link add name cloudover0  type dummy', shell=True)
        system.call('ip addr add  169.254.169.254 dev cloudover0', shell=True)
        system.call('ip link set cloudover0 up', shell=True)


    def _restart_services(self):
        log(msg="restart_services: restarting quagga (debian and/or redhat version)", tags=('system', 'info'))
        system.call('service quagga restart', shell=True)
        system.call('service ospfd restart', shell=True)
        system.call('service zebra restart', shell=True)
        system.call('service nginx restart', shell=True)

        log(msg="restart_services: restarting libvirt (debian and/or redhat version)", tags=('system', 'info'))
        system.call('service libvirtd restart', shell=True)
        system.call('service libvirt-bin restart', shell=True)


    def configure_node(self):
        super(Driver, self).configure_node()
        self._register_node()
        self._setup_quagga(core=False)


    def startup_node(self):
        super(Driver, self).startup_node()

        self._setup_cloudinit()
        self._restart_services()
        self._update_state('ok', 'Node services started')


    def shutdown_node(self):
        self._update_state('offline', 'Node is going offline')
        super(Driver, self).shutdown_node()


    def configure_core(self):
        super(Driver, self).configure_core()
        self._check_i_am_root()

        self._setup_quagga(core=True)
        self._restart_services()
