# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# coding: utf-8
# pylint: skip-file
from msrest.serialization import Model


class CustomImage(Model):
    """A custom image.

    :param vm: The virtual machine from which the image is to be created.
    :type vm: :class:`CustomImagePropertiesFromVm
     <azure.mgmt.devtestlabs.models.CustomImagePropertiesFromVm>`
    :param vhd: The VHD from which the image is to be created.
    :type vhd: :class:`CustomImagePropertiesCustom
     <azure.mgmt.devtestlabs.models.CustomImagePropertiesCustom>`
    :param description: The description of the custom image.
    :type description: str
    :param author: The author of the custom image.
    :type author: str
    :param creation_date: The creation date of the custom image.
    :type creation_date: datetime
    :param managed_image_id: The Managed Image Id backing the custom image.
    :type managed_image_id: str
    :param provisioning_state: The provisioning status of the resource.
    :type provisioning_state: str
    :param unique_identifier: The unique immutable identifier of a resource
     (Guid).
    :type unique_identifier: str
    :param id: The identifier of the resource.
    :type id: str
    :param name: The name of the resource.
    :type name: str
    :param type: The type of the resource.
    :type type: str
    :param location: The location of the resource.
    :type location: str
    :param tags: The tags of the resource.
    :type tags: dict
    """

    _attribute_map = {
        'vm': {'key': 'properties.vm', 'type': 'CustomImagePropertiesFromVm'},
        'vhd': {'key': 'properties.vhd', 'type': 'CustomImagePropertiesCustom'},
        'description': {'key': 'properties.description', 'type': 'str'},
        'author': {'key': 'properties.author', 'type': 'str'},
        'creation_date': {'key': 'properties.creationDate', 'type': 'iso-8601'},
        'managed_image_id': {'key': 'properties.managedImageId', 'type': 'str'},
        'provisioning_state': {'key': 'properties.provisioningState', 'type': 'str'},
        'unique_identifier': {'key': 'properties.uniqueIdentifier', 'type': 'str'},
        'id': {'key': 'id', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
        'location': {'key': 'location', 'type': 'str'},
        'tags': {'key': 'tags', 'type': '{str}'},
    }

    def __init__(self, vm=None, vhd=None, description=None, author=None, creation_date=None, managed_image_id=None, provisioning_state=None, unique_identifier=None, id=None, name=None, type=None, location=None, tags=None):
        self.vm = vm
        self.vhd = vhd
        self.description = description
        self.author = author
        self.creation_date = creation_date
        self.managed_image_id = managed_image_id
        self.provisioning_state = provisioning_state
        self.unique_identifier = unique_identifier
        self.id = id
        self.name = name
        self.type = type
        self.location = location
        self.tags = tags
