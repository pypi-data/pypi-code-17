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
import pwd
import random
import hashlib
import base64
import netaddr
import netifaces
import shutil
import django.conf
from django.template import Context, Template
from corenetwork.utils import system, config
from corenetwork.utils.logger import log

class CorosyncMixin():
    """
    Add corosync related functions
    """
    def _corosync_keygen(self):
        '''
        Generate new authkey if doesn't exists and copy it to cloudover's home
        '''
        log(msg='corosync_keygen: configuring auth key', tags=('system', 'info'))
        key_path = '/etc/corosync/authkey'
        if not os.path.exists(key_path):
            system.call('corosync-keygen')
        shutil.copyfile(key_path, '/var/lib/cloudOver/corosync_auth')
        os.chmod(key_path, 0600)
        os.chown(key_path, pwd.getpwnam('cloudover').pw_uid, pwd.getpwnam('cloudover').pw_gid)


    def _corosync_configure(self, core=False):
        '''
        Create config for corosync (at node or at core)
        '''
        auth_seed = hashlib.sha256(str(random.random())).hexdigest()

        networks_vxlan = netifaces.ifaddresses(config.get('network', 'VXLAN_INTERFACE'))
        networks = []
        if 2 in networks_vxlan:
            for ip in networks_vxlan[2]:
                addr = str(netaddr.IPNetwork('%s/%s' % (ip['addr'], ip['netmask'])).cidr)
                networks.append(addr)

        networks = [n.split('/')[0] for n in networks]

        if core:
            try:
                django.conf.settings.configure()
            except:
                pass
            auth_key = open('/var/lib/cloudOver/corosync_auth', 'r').read(1024*1024*16)
            t = Template(open('/etc/corenetwork/drivers/corosync/config.xml', 'r').read(1024*1024*16))
            config_contents = t.render(Context({'networks': networks}))
        else:
            auth_key = base64.b64decode(self._request('/ci/corosync/get_auth_key/', {'auth_hash': self._calc_hash(config.get('node', 'AUTH_TOKEN'), auth_seed),
                                                                                     'auth_seed': auth_seed}))
            config_contents = self._request('/ci/corosync/get_config/', {'auth_hash': self._calc_hash(config.get('node', 'AUTH_TOKEN'), auth_seed),
                                                                         'auth_seed': auth_seed,
                                                                         'networks': networks})

            auth_key_file = open('/etc/corosync/authkey', 'w')
            auth_key_file.write(auth_key)
            auth_key_file.close()
            os.chmod('/etc/corosync/authkey', 0400)

        config_file = open('/etc/corosync/corosync.conf', 'w')
        config_file.write(config_contents)
        config_file.close()

        corosync_defaults = open('/etc/default/corosync', 'w')
        corosync_defaults.write('START=yes\n')
        corosync_defaults.close()

        system.call('service corosync restart', shell=True)
        system.call('service sheepdog restart', shell=True)
