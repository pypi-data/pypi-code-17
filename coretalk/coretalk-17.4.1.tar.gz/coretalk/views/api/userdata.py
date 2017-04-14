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


from coretalk.models.coretalk.userdata import UserData

from corecluster.utils.exception import CoreException
from corecluster.models.core import VM, Image
from corecluster.cache.task import Task
from corecluster.cache.data_chunk import DataChunk
from corecluster.utils.decorators import register
from corecluster.utils import validation as v

from corenetwork.utils import system

import base64
import os
import pyaml
import simplejson


@register(auth='token', validate={'name': v.is_string()})
def create(context, name, data, convert_from=None):
    '''
    Create new UserData object
    :param name: Name of userdata script
    :param data: Contents of script
    :param convert_from: Detemines if script should be converted from another format to yaml. By default don't try to
    convert. Possible options: yaml, json, native (native list or dictionaries, sent in request's format)
    '''
    userdata = UserData()
    userdata.name = name
    if convert_from is None:
        userdata.data = data
    elif convert_from == 'native':
        userdata.data = '#cloud-config\n' + pyaml.dumps(data)
    elif convert_from == 'pyaml':
        userdata.data = '#cloud-config\n' + pyaml.dumps(pyaml.loads(data))
    elif convert_from == 'json':
        userdata.data = '#cloud-config\n' + pyaml.dumps(simplejson.loads(data))
    else:
        raise CoreException('unsupported_format')

    userdata.user_id = context.user_id
    userdata.save()

    return userdata.to_dict


@register(auth='token', validate={'userdata_id': v.is_id()})
def edit(context, userdata_id, **kwargs):
    """ Edit VM properties """
    ud = UserData.get(context.user_id, userdata_id)
    ud.edit(context, **kwargs)
    ud.save()

    return ud.to_dict


@register(auth='token', validate={'userdata_id': v.is_id()})
def delete(context, userdata_id):
    userdata = UserData.get(context.user_id, userdata_id)
    userdata.remove(context)


@register(auth="token")
def get_list(context):
    """
    Returns list of all userdata objects in cloud
    """
    userdata = UserData.get_list(context.user_id)
    return [ud.to_dict for ud in userdata]


@register(auth="token", validate={'userdata_id': v.is_id()})
def get_by_id(context, userdata_id):
    """
    Returns userdata object identified by id
    """
    return UserData.get(context.user_id, userdata_id).to_dict


@register(auth='token', validate={'userdata_id': v.is_id(), 'vm_id': v.is_id()})
def attach(context, userdata_id, vm_id):
    """
    Attach userdata object to vm (it is accessible via http://169.254.169.254/latest/user-data/)
    :param userdata_id: id of userdata object
    :param vm_id: id ov vm
    """
    userdata = UserData.get(context.user_id, userdata_id)
    vm = VM.get(context.user_id, vm_id)

    vm.set_prop('coretalk_user_data', userdata_id)
    vm.save()


@register(auth='token')
def attach_configdrive(context, userdata_id, vm_id):
    userdata = UserData.get(context.user_id, userdata_id)
    vm = VM.get(context.user_id, vm_id)

    system.call(['mkdir', '-p', '/tmp/configdrive_' + userdata.id + '/openstack/latest/'])
    ud = open('/tmp/configdrive_' + userdata.id + '/openstack/latest/user_data', 'w')
    ud.write(userdata.data)
    ud.close()

    # Detailed instruction: https://coreos.com/os/docs/latest/config-drive.html
    #TODO: Convert to: http://serverfault.com/questions/43634/how-to-mount-external-vfat-drive-as-user
    system.call(['genisoimage', '-R', '-V', 'config-2', '-o', '/tmp/configdrive_' + userdata.id + '.img', '/tmp/configdrive_' + userdata.id])
    system.call(['rm', '-rf', '/tmp/configdrive_' + userdata.id])
    system.call(['qemu-img', 'convert', '-f', 'raw', '-O', 'qcow2', '/tmp/configdrive_' + userdata.id + '.img', '/tmp/configdrive_' + userdata.id + '.qcow2'])
    system.call(['rm', '-rf', '/tmp/configdrive_' + userdata.id + '.img'])

    image = Image.create(name='CoreTalk ConfigDrive',
                         description='UserData: %s, VM: %s' % (userdata.id, vm.id),
                         access='private',
                         format='qcow2',
                         size=os.stat('/tmp/configdrive_' + userdata.id + '.qcow2').st_size,
                         type='permanent',
                         disk_controller='virtio',
                         user=vm.user)
    image.save()

    create_img = Task()
    create_img.user_id = context.user_id
    create_img.type = 'image'
    create_img.action = 'create'
    create_img.append_to([vm, image, image.storage])

    chunk = DataChunk()
    contents = open('/tmp/configdrive_' + userdata.id + '.qcow2').read(image.size)
    chunk.data = base64.b64encode(contents)
    chunk.offset = 0
    chunk.image_id = image.id
    chunk.type = 'upload'
    chunk.save()

    upload_data = Task()
    upload_data.user_id = context.user_id
    upload_data.type = 'image'
    upload_data.action = 'upload_data'
    upload_data.set_all_props({'offset': 0,
                               'size': image.size,
                               'chunk_id': chunk.cache_key()})
    upload_data.append_to([image, vm])

    attach_img = Task()
    attach_img.user_id = context.user_id
    attach_img.type = 'image'
    attach_img.action = 'attach'
    attach_img.append_to([vm, image])


@register(auth='token', validate={'vm_id': v.is_id()})
def detach(context, vm_id):
    """ Detach userdata from vm instance
    :param vm_id: id of virtual machine
    :return:
    """
    vm = VM.get(context.user_id, vm_id)

    all_props = vm.get_all_props()
    if 'coretalk_user_data' in all_props:
        del all_props['coretalk_user_data']

    vm.set_all_props(all_props)
    vm.save()


@register(auth='token')
def describe(context):
    """ Show serializable and editable fields in model """
    return UserData.describe_model()
