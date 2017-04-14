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

import re
import netaddr
import netifaces
import requests
import simplejson
from corenetwork.utils import system, config
from corenetwork.utils.logger import log
from distutils.version import StrictVersion


class NetworkMixin():
    def _get_interface_list(self):
        """
        Get list of interfaces available in system and enabled in config (regexps are accepted)
        """
        interfaces = []
        # Iterate over patterns and names in config
        for interface_config in config.get('network', 'INTERFACES', []):
            # Iterate over all interfaces known in OS
            for iface in netifaces.interfaces():
                if re.match(interface_config['iface'], iface):
                    interface = {
                        'iface': iface,
                        'cost': interface_config['cost'],
                    }

                    # Get networks assigned to interface
                    addrs = netifaces.ifaddresses(iface)
                    if not 2 in addrs:
                        continue
                    interface['networks'] = []
                    for ip in addrs[2]:
                        addr = str(netaddr.IPNetwork('%s/%s' % (ip['addr'], ip['netmask'])).cidr)
                        interface['networks'].append(addr)

                    interfaces.append(interface)

        return interfaces


    def _initialize_iptables(self):
        """
        Add iptables chains for redirections and VNC
        """
        null = open('/dev/null', 'w')

        # Public leases
        system.call('sudo iptables -t nat -N CORE_REDIRECTION_DNAT', shell=True, stderr=null)
        system.call('sudo iptables -t nat -D PREROUTING -j CORE_REDIRECTION_DNAT', shell=True)
        system.call('sudo iptables -t nat -A PREROUTING -j CORE_REDIRECTION_DNAT', shell=True)


        system.call('echo 1 | sudo tee /proc/sys/net/ipv4/conf/all/promote_secondaries', shell=True, stdout=null)
        system.call('echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward', shell=True, stdout=null)

        # VNC
        r = system.call('sudo iptables -t nat -N CORE_VNC_DNAT', shell=True)
        if r == 0:
            system.call('sudo iptables -t nat -A CORE_VNC_DNAT -j RETURN', shell=True)
            system.call('sudo iptables -t nat -A PREROUTING -j CORE_VNC_DNAT', shell=True)

            system.call('sudo iptables -t nat -N CORE_VNC_MASQ', shell=True)
            system.call('sudo iptables -t nat -A CORE_VNC_MASQ -j RETURN', shell=True)
            system.call('sudo iptables -t nat -A POSTROUTING -j CORE_VNC_MASQ', shell=True)

        system.call('echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward', shell=True, stdout=null)

        from corecluster.models.core import VM
        from corecluster.cache.task import Task
        for vm in VM.objects.filter(vnc_enabled=True).exclude(state__in=['closed', 'failed', 'closing']).all():
            t = Task()
            t.type = 'console'
            t.action = 'attach_vnc'
            t.append_to([vm])

        null.close()


    def _cleanup_iptables(self):
        """
        Remove iptables chains
        """
        null = open('/dev/null', 'w')

        # Public leases
        system.call('sudo iptables -t nat -D PREROUTING -j CORE_REDIRECTION_DNAT', shell=True, stderr=null)
        system.call('sudo iptables -t nat -X CORE_REDIRECTION_DNAT', shell=True, stderr=null)

        # VNC
        system.call('sudo iptables -t nat -D PREROUTING -j CORE_VNC_DNAT', shell=True, stderr=null)
        system.call('sudo iptables -t nat -D POSTROUTING -j CORE_VNC_MASQ', shell=True, stderr=null)
        system.call('sudo iptables -t nat -F CORE_VNC_DNAT', shell=True, stderr=null)
        system.call('sudo iptables -t nat -F CORE_VNC_MASQ', shell=True, stderr=null)
        system.call('sudo iptables -t nat -X CORE_VNC_DNAT', shell=True, stderr=null)
        system.call('sudo iptables -t nat -X CORE_VNC_MASQ', shell=True, stderr=null)

        null.close()

    def _check_updates(self, component, id='none', current_version=None):
        '''
        Check for updates for component. If current_version is set, return True when newer version is available.
        '''

        if current_version == None:
            try:
                from corecluster import version
                current_version = version.version
            except:
                current_version = 'none'

        try:
            r = requests.get('http://updates.cloudover.org/' + component + '?id=' + id + '&version=' + str(current_version))

            info = simplejson.JSONDecoder().decode(r.text)
            if current_version is not None:
                return StrictVersion(info['latest']) > StrictVersion(current_version)
            else:
                log(msg='Latest version of CoreCluster is %s' % str(info['latest']), tags=('system', 'info'))
        except:
            pass