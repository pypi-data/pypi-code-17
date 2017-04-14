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


from coretalk.models.coretalk.sshkey import SshKey

from corecluster.models.core.vm import VM
from corecluster.utils.decorators import register
from corecluster.utils import validation as v


@register(auth='token', validate={'name': v.is_string(), 'public_key': v.is_string()})
def create(context, name, public_key):
    key = SshKey()
    key.name = name
    key.key = public_key
    key.user_id = context.user_id
    key.save()

    return key.to_dict


@register(auth='token', validate={'key_id': v.is_id()})
def edit(context, key_id, **kwargs):
    k = SshKey.get(context.user_id, key_id)
    k.edit(context, **kwargs)
    k.save()

    return k.to_dict


@register(auth='token', validate={'key_id': v.is_id()})
def delete(context, key_id):
    k = SshKey.get(context.user_id, key_id)
    k.remove(context)


@register(auth="token")
def get_list(context):
    keys = SshKey.get_list(context.user_id)
    return [k.to_dict for k in keys]


@register(auth="token", validate={'key_id': v.is_id()})
def get_by_id(context, key_id):
    return SshKey.get(context.user_id, key_id).to_dict


@register(auth='token', validate={'key_id': v.is_id(), 'vm_id': v.is_id()})
def attach(context, key_id, vm_id):
    k = SshKey.get(context.user_id, key_id)
    vm = VM.get(context.user_id, vm_id)

    vm.set_prop('coretalk_ssh_key', k.id)
    vm.save()


@register(auth='token', validate={'vm_id': v.is_id()})
def detach(context, vm_id):
    vm = VM.get(context.user_id, vm_id)

    all_props = vm.get_all_props()
    if 'coretalk_ssh_key' in all_props:
        del all_props['coretalk_ssh_key']

    vm.set_all_props(all_props)
    vm.save()


@register(auth='token')
def describe(context):
    """ Show serializable and editable fields in model """
    return SshKey.describe_model()