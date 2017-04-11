# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import json
import requests

from datetime import timedelta

from .models.enum_user_role import EnumUserRole
from .models.enum_user_type import EnumUserType

from .exceptions import RedOctoberDecryptException
from .exceptions import RedOctoberRemoteException


class RedOctober(object):
    """ It provides Python bindings to a remote RedOctober server via HTTP(S).

    Additional documentation regarding the API endpoints is available at
    https://github.com/cloudflare/redoctober
    """

    def __init__(self, host, port, name, password, ssl=True, verify=True):
        """ It initializes the RedOctober API using the provided credentials.

        Args:
            host (str): Host name/IP of Red October server.
            port (int): Port number of server.
            name (str): Account name for use as login.
            password (str): Password for account.
            ssl (bool): Is server SSL encrypted?
            verify (bool or str): File path of CA cert for verification,
                `True` to use system certs, or `False` to disable certificate
                verification.
        """
        ssl = 'https' if ssl else 'http'
        self.uri_base = '%s://%s:%d' % (ssl, host, port)
        self.name = name
        self.password = password
        self.verify = verify

    def create_vault(self):
        """ It creates a new vault.

        Create is the necessary first call to a new vault.
        It creates an admin account.

        Returns:
            bool: Status of vault creation
        """
        return self.call('create')

    def delegate(self, time=None, uses=None):
        """ It allows for the delegation of decryption rights.

        Delegate allows a user to delegate their decryption password to the
        server for a fixed period of time and for a fixed number of
        decryptions. If the user's account is not created, it creates it.
        Any new delegation overrides the previous delegation.

        Args:
            time (datetime.timedelta): Period of time that delegation is valid
                for.
            uses (int): Number of times that delegation can be used.
        Returns:
            bool: Status of delegation creation.
        """
        data = self._clean_mapping({
            'Time': time and '%ds' % time.total_seconds() or None,
            'Uses': uses,
        })
        return self.call('delegate', data=data)

    def create_user(self, user_type='rsa'):
        """ It creates a new user account.

        Allows an optional ``UserType`` to be specified which controls how the
        record is encrypted. This can have a value of either ``rsa`` or ``ecc``
        and if none is provided will default to ``rsa``.

        Args:
            user_type (str): Controls how the record is encrypted. This can have
                a value of either ``ecc`` or ``rsa``.
        Returns:
            bool: Status of user creation.
        """
        data = self._clean_mapping({
            'UserType': EnumUserType[user_type].name.upper(),
        })
        return self.call('create-user', data=data)

    def get_summary(self):
        """ It provides a list of keys and delegations for the server.

        Returns:
            dict: A mapping containing keys on the system, and users who have
                currently delegated their key to the server. Example:

                .. code-block:: python

                    {
                    "Live":{
                    "Bill":{"Admin":false,
                            "Type":"rsa",
                            "Expiry":"2013-11-26T08:42:29.65501032-08:00",
                            "Uses":3},
                    "Cat":{"Admin":false,
                           "Type":"rsa",
                           "Expiry":"2013-11-26T08:42:42.016311595-08:00",
                           "Uses":3},
                    "Dodo":{"Admin":false,
                            "Type":"rsa",
                            "Expiry":"2013-11-26T08:43:06.651429104-08:00",
                            "Uses":3}
                   },
                   "All":{
                    "Alice":{"Admin":true, "Type":"rsa"},
                    "Bill":{"Admin":false, "Type":"rsa"},
                    "Cat":{"Admin":false, "Type":"rsa"},
                    "Dodo":{"Admin":false, "Type":"rsa"}
                   }
        """
        return self.call('summary')

    def encrypt(self, minimum, owners, data):
        """ It allows a user to encrypt a piece of data.

        Args:
            minimum (int): Minimum number of users from ``owners`` set that
                must have delegated their keys to the server.
            owners (iter): Iterator of strings indicating users that may
                decrypt the document.
            data (str): Data to encrypt.
        Returns:
            str: Base64 encoded string representing the encrypted string.
        """
        data = self._clean_mapping({
            'Minimum': minimum,
            'Owners': owners,
            'Data': data.encode('base64'),
        })
        return self.call('encrypt', data=data)

    def decrypt(self, data):
        """ It allows a user to decrypt a piece of data.

        Args:
            data (str): Base64 encoded string representing the encrypted
                string.
        Raises:
            RedOctoberDecryptException: If not enough ``minimum`` users from
                the set of ``owners`` have delegated their keys to the server,
                or if the decryption credentials are incorrect.
        Returns:
            dict: Response object with the following keys:
                * `Data` (`str`): Decrypted data
                * `Secure` (`bool`): Not documented. Seems to always be `True`
                * `Delegates` (`list` of `str`): Delegate names
        """
        data = self._clean_mapping({
            'Data': data,
        })
        try:
            response = self.call('decrypt', data=data)
            response = json.loads(response.decode('base64'))
            response['Data'] = response['Data'].decode('base64')
            return response
        except RedOctoberRemoteException as e:
            raise RedOctoberDecryptException(e.message)

    def get_owners(self, data):
        """ It provides the delegates required to decrypt a piece of data.

        Args:
            data (str): Base64 encoded string representing the encrypted
                string.
        Raises:
            RedOctoberDecryptException: If incorrect decryption credentials
                are provided.
        Returns:
            list: List of strings representing users that are able to decrypt
                the data.
        """
        data = self._clean_mapping({
            'Data': data,
        })
        try:
            return self.call('owners', data=data)
        except RedOctoberRemoteException as e:
            raise RedOctoberDecryptException(e.message)

    def change_password(self, new_password):
        """ It allows users to change their password.

        Args:
            name (str): Name of account.
            password (str): Password for account.
            new_password (str): New password for account.
        Returns:
            bool: Password change status.
        """
        data = self._clean_mapping({
            'NewPassword': new_password,
        })
        return self.call('password', data=data)

    def modify_user_role(self, modify_name, command='revoke'):
        """ It allows for administration of user roles.

        Args:
            modify_name (str): Name of account to modify.
            command (str): Command to apply to user:
                ``admin``: Promote user to administrator.
                ``revoke``: Revoke administrator rights.
                ``delete``: Delete user.
        Returns:
            bool: Role modfication status.
        """
        data = self._clean_mapping({
            'ToModify': modify_name,
            'Command': EnumUserRole[command].name,
        })
        return self.call('modify', data=data)

    def purge_delegates(self):
        """ It deletes all delegates for an encryption key.

        Returns:
            bool: Purge status.
        """
        return self.call('purge')

    def create_order(self, labels, duration, uses, data):
        """ It creates lets others users know delegations are needed.

        Args:
            labels (iter): Iterator of strings to label order with.
            duration (datetime.timedelta): Proposed duration of delegation.
            uses (int): Proposed delegation use amounts.
            data (str): Base64 encoded string representing the encrypted
                string.
        Returns:
            dict: Mapping representing the newly created order. Example:

            .. code-block:: python

                {
                    "Admins": [
                         "Bob",
                         "Eve"
                     ],
                     "AdminsDelegated": null,
                     "Delegated": 0,
                     "DurationRequested": 3.6e+12,
                     "Labels": [
                         "blue",
                         "red"
                     ],
                     "Name": "Alice",
                     "Num": "77da1cfd8962fb9685c15c84",
                     "TimeRequested": "2016-01-25T15:58:41.961906679-08:00",
                 }
        """
        data = self._clean_mapping({
            'Labels': labels,
            'Duration': '%ds' % duration.total_seconds(),
            'Uses': uses,
            'Data': data,
        })
        return self.call('order', data=data)

    def get_orders_outstanding(self):
        """ It returns a mapping of current orders.

        Returns:
            dict: Mapping representing the currently open orders. Example:

            .. code-block:: python

                {
                    "77da1cfd8962fb9685c15c84":{
                        "Name":"Alice",
                        "Num":"77da1cfd8962fb9685c15c84",
                        "TimeRequested":"2016-01-25T15:58:41.961906679-08:00",
                        "DurationRequested":3600000000000,
                        "Delegated":0,"
                        AdminsDelegated":null,
                        "Admins":["Bob, Eve"],
                        "Labels":["Blue","Red"]
                    }
                }
        """
        return self.call('orderout')

    def get_order_information(self, order_num):
        """ It gets information for a specified order.

        Args:
            order_num (str): Order number to get.
        Returns:
            dict: Mapping representing the order information. Example:

            .. code-block:: python

                {
                    "Admins": [
                        "Bob",
                        "Eve"
                    ],
                    "AdminsDelegated": null,
                    "Delegated": 0,
                    "DurationRequested": 3.6e+12,
                    "Labels": [
                        "blue",
                        "red"
                    ],
                    "Name": "Alice",
                    "Num": "77da1cfd8962fb9685c15c84",
                    "TimeRequested": "2016-01-25T15:58:41.961906679-08:00"
                }
        """
        data = self._clean_mapping({
            'OrderNum': order_num,
        })
        return self.call('orderinfo', data=data)

    def cancel_order(self, order_num):
        """ It cancels an order by number.

        Args:
            order_num (str): Order number to get.
        Returns:
            bool: Status of order cancellation.
        """
        data = self._clean_mapping({
            'OrderNum': order_num,
        })
        return self.call('ordercancel', data=data)

    def call(self, endpoint, method='POST', params=None, data=None):
        """ It calls the remote endpoint and returns the result, if success.

        Args:
            endpoint (str): RedOctober endpoint to call (e.g. ``newcert``).
            method (str): HTTP method to utilize for the Request.
            params: (dict or bytes) Data to be sent in the query string
                for the Request.
            data: (dict or bytes or file) Data to send in the body of the
                Request.
        Raises:
            RedOctoberRemoteException: In the event of a ``False`` in the
                ``success`` key of the API response.
        Returns:
            mixed: Data contained in ``result`` key of the API response, or
                ``True`` if there was no response data, but the call was a
                success.
        """
        endpoint = '%s/%s' % (self.uri_base, endpoint)
        if data is None:
            data = {}
        data.update({
            'Name': self.name,
            'Password': self.password,
        })
        response = requests.request(
            method=method,
            url=endpoint,
            params=params,
            json=data,
            verify=self.verify,
        )
        response = response.json()
        if response['Status'] != 'ok':
            raise RedOctoberRemoteException(
                response['Status'],
            )
        try:
            return response['Response']
        except KeyError:
            return True

    def _clean_mapping(self, mapping):
        """ It removes false entries from mapping.

        Args:
            mapping (dict): Mapping to remove values from.
        Returns:
            dict: Mapping with no values evaluating to False.
        """
        return {k:v for k, v in mapping.iteritems() if v}
