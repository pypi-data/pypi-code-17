# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# coding: utf-8
# pylint: skip-file
from msrest.serialization import Model


class UserSecretStore(Model):
    """Properties of a user's secret store.

    :param key_vault_uri: The URI of the user's Key vault.
    :type key_vault_uri: str
    :param key_vault_id: The ID of the user's Key vault.
    :type key_vault_id: str
    """

    _attribute_map = {
        'key_vault_uri': {'key': 'keyVaultUri', 'type': 'str'},
        'key_vault_id': {'key': 'keyVaultId', 'type': 'str'},
    }

    def __init__(self, key_vault_uri=None, key_vault_id=None):
        self.key_vault_uri = key_vault_uri
        self.key_vault_id = key_vault_id
