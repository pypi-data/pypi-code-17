# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# coding: utf-8
# pylint: skip-file
from msrest.serialization import Model


class ComputeVmInstanceViewStatus(Model):
    """ComputeVmInstanceViewStatus.

    :param code: Gets the status Code.
    :type code: str
    :param display_status: Gets the short localizable label for the status.
    :type display_status: str
    """

    _attribute_map = {
        'code': {'key': 'code', 'type': 'str'},
        'display_status': {'key': 'displayStatus', 'type': 'str'},
    }

    def __init__(self, code=None, display_status=None):
        self.code = code
        self.display_status = display_status
