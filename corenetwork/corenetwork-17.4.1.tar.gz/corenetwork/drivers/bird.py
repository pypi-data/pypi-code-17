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

# import os
# import re
# import sys
# import netaddr
# import datetime
# import netifaces
# from corenetwork.utils import system
#
# sys.path.append('/etc/cloudOver/')
# sys.path.append('/usr/lib/cloudOver/')
#
# from django.template import loader, Context
#
#
# def get_interface_list():
#     interfaces = []
#     enabled_interfaces = [iface['iface'] for iface in networkConf.interfaces]
#     for iface in netifaces.interfaces():
#         for iface_name in enabled_interfaces:
#             if re.match(iface_name, iface):
#                 interfaces.append(iface)
#     return interfaces
#
# def restart_services():
#     if os.path.exists('/etc/init.d/bird'):
#         system.call('/etc/init.d/quagga restart', shell=True)
#
#
# def configure(ospf_token):
#     """
#     :param ospf_token: OSPF token used to authenticate cluster nodes itself.
#     """
#     if not os.path.exists('/etc/corenetwork/drivers/bird/bird.conf'):
#         raise Exception('Cannot find configuration templates')
#
#     if os.path.exists('/etc/bird.conf'):
#         os.rename('/etc/bird.conf', '/etc/bird.conf.%s' % str(datetime.datetime.now()))
#
#     interfaces = get_interface_list()
#     hostname = open('/proc/sys/kernel/hostname', 'r').read()
#     password = networkConf.QUAGGA_PASSWORD
#     router_id = None
#     networks = []
#
#     for iface in interfaces:
#         addrs = netifaces.ifaddresses(iface)
#         # IPv4 addresses
#         if not 2 in addrs:
#             continue
#
#         for ip in addrs[2]:
#             addr = str(netaddr.IPNetwork('%s/%s' % (ip['addr'], ip['netmask'])).cidr)
#             networks.append(addr)
#             # Set router_id to first interface from list
#             if router_id == None:
#                 router_id = ip['addr']
#
#     c = Context({
#         'interfaces': interfaces,
#         'hostname': hostname,
#         'password': password,
#         'ospf_token': ospf_token,
#         'router_id': router_id,
#         'networks': networks
#     })
#     if loader.settings.configured:
#         dirs = list(loader.settings.TEMPLATE_DIRS)
#         dirs.append('/etc/cloudOver/networkConf/')
#         loader.settings.TEMPLATE_DIRS = dirs
#     else:
#         loader.settings.configure(TEMPLATE_DIRS=['/etc/cloudOver/networkConf/drivers/bird'], DEBUG=True)
#
#     bird_template = loader.get_template("bird.conf")
#
#     bird_conf = open('/etc/bird.conf', 'w')
#     bird_conf.write(bird_template.render(c))
#     bird_conf.close()
#
