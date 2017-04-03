# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# coding: utf-8
# pylint: skip-file
from msrest.serialization import Model


class ApplyArtifactsRequest(Model):
    """Request body for applying artifacts to a virtual machine.

    :param artifacts: The list of artifacts to apply.
    :type artifacts: list of :class:`ArtifactInstallProperties
     <azure.mgmt.devtestlabs.models.ArtifactInstallProperties>`
    """

    _attribute_map = {
        'artifacts': {'key': 'artifacts', 'type': '[ArtifactInstallProperties]'},
    }

    def __init__(self, artifacts=None):
        self.artifacts = artifacts
