# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# coding: utf-8
# pylint: skip-file
from msrest.serialization import Model


class ArmTemplateParameterProperties(Model):
    """Properties of an Azure Resource Manager template parameter.

    :param name: The name of the template parameter.
    :type name: str
    :param value: The value of the template parameter.
    :type value: str
    """

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'value': {'key': 'value', 'type': 'str'},
    }

    def __init__(self, name=None, value=None):
        self.name = name
        self.value = value
