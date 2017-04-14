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


from django.http import HttpResponse

import netaddr

from corecluster.models.core.lease import Lease
from corecluster.models.core.network_pool import NetworkPool
from coretalk.models.coretalk.userdata import UserData
from coretalk.models.coretalk.sshkey import SshKey
from corenetwork.utils.logger import log


def resolve_ip(auth_hash, auth_seed, vm_ip):
    addr = netaddr.IPAddress(vm_ip)
    for network in NetworkPool.objects.all():
        if addr >= network.to_ipnetwork().network and addr <= network.to_ipnetwork().broadcast:
            if network.mode == 'routed':
                lease = Lease.objects.filter(subnet__network_pool_id=network.id).get(address=str(addr-2))
                lease.vm.node.check_auth(auth_hash, auth_seed)
                return lease
    raise Exception('lease_not_found')


def get_root(request, auth_hash, auth_seed, vm_ip):
    return HttpResponse('latest\n')

def get_latest(request, auth_hash, auth_seed, vm_ip):
    return HttpResponse('meta-data\nuser-data\n')

def get_meta_data(request, auth_hash, auth_seed, vm_ip):
    return HttpResponse('ami-id\nhostname\ninstance-id\ninstance-type\npublic-keys\n')


# Meta-data Functions
def get_ami_id(request, auth_hash, auth_seed, vm_ip):
    try:
        lease = resolve_ip(auth_hash, auth_seed, vm_ip)
    except:
        return HttpResponse('none')

    vm = lease.vm
    if vm == None:
        return HttpResponse('none')

    if vm.base_image == None:
        return HttpResponse('none')

    return HttpResponse(vm.base_image.id)


def get_hostname(request, auth_hash, auth_seed, vm_ip):
    try:
        lease = resolve_ip(auth_hash, auth_seed, vm_ip)
    except:
        return HttpResponse('none')

    return HttpResponse(lease.hostname)


def get_instance_id(request, auth_hash, auth_seed, vm_ip):
    try:
        lease = resolve_ip(auth_hash, auth_seed, vm_ip)
    except:
        return HttpResponse('none')

    vm = lease.vm
    if vm == None:
        return HttpResponse('none')

    return HttpResponse(vm.id)


def get_instance_type(request, auth_hash, auth_seed, vm_ip):
    try:
        lease = resolve_ip(auth_hash, auth_seed, vm_ip)
    except:
        return HttpResponse('none')

    vm = lease.vm
    if vm == None:
        return HttpResponse('none')

    return HttpResponse(vm.template.ec2name)


def get_public_keys(request, auth_hash, auth_seed, vm_ip):
    try:
        lease = resolve_ip(auth_hash, auth_seed, vm_ip)
    except:
        return HttpResponse('none')

    vm = lease.vm
    if vm == None:
        return HttpResponse('none')

    try:
        keys = vm.get_prop("coretalk_keys")
        key_list = ''
        for k in keys:
            key = SshKey.objects.get(id=k)
            key_list += key.id + '=' + key.name + '\n'
        return HttpResponse(key_list)
    except:
        return HttpResponse('none')


def get_ssh_key_formats(request, auth_hash, auth_seed, vm_ip, id):
    try:
        lease = resolve_ip(auth_hash, auth_seed, vm_ip)
    except:
        return HttpResponse('none')

    vm = lease.vm
    if vm == None:
        return HttpResponse('none')

    print "openssh-key"


def get_ssh_key_formats(request, auth_hash, auth_seed, vm_ip, id):
    try:
        lease = resolve_ip(auth_hash, auth_seed, vm_ip)
    except:
        return HttpResponse('none')

    vm = lease.vm
    if vm == None:
        return HttpResponse('none')

    key = SshKey.objects.get(id=id)
    return HttpResponse(key.key)


def get_user_data(request, auth_hash, auth_seed, vm_ip):
    log(msg='Serving cloudinit for %s' % vm_ip, tags=('coretalk', 'debug'))
    try:
        lease = resolve_ip(auth_hash, auth_seed, vm_ip)
    except:
        return HttpResponse('none')

    vm = lease.vm
    if vm == None:
        return HttpResponse('none')

    try:
        user_data_id = vm.get_prop('coretalk_user_data')
    except:
        return HttpResponse('none')

    try:
        user_data = UserData.objects.get(id=user_data_id)
        return HttpResponse(user_data.data)
    except:
        return HttpResponse('none')

