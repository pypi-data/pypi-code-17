# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# coding: utf-8
# pylint: skip-file
from msrest.serialization import Model


class WindowsOsInfo(Model):
    """Information about a Windows OS.

    :param windows_os_state: The state of the Windows OS (i.e. NonSysprepped,
     SysprepRequested, SysprepApplied). Possible values include:
     'NonSysprepped', 'SysprepRequested', 'SysprepApplied'
    :type windows_os_state: str or :class:`WindowsOsState
     <azure.mgmt.devtestlabs.models.WindowsOsState>`
    """

    _attribute_map = {
        'windows_os_state': {'key': 'windowsOsState', 'type': 'str'},
    }

    def __init__(self, windows_os_state=None):
        self.windows_os_state = windows_os_state
