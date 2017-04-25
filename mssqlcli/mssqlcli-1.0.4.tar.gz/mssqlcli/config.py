"""Keyring Access for python-mssqlclient."""
# Copyright (C) 2016 Russell Troxel

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import re

import keyring
import yaml


class Config(object):
    """
    Config object to unmarshall YAML configuration files.

    Automatically supports keyring entries for all variables EXCEPT
    keyring_app_name, which must be a local string.

    All top-level keys are converted to attributes.
    """

    matcher = re.compile(r'^USE_KEYRING\([\'\"](.*)[\'\"]\)$')

    def __init__(self, config_file):
        """
        Config object to unmarshall YAML configuration files.

        Automatically supports keyring entries for all variables EXCEPT
        keyring_app_name, which must be a local string.

        All top-level keys are converted to attributes.

        :param string config_file: location of YAML file to be unmarshalled.
        :rtype: :class:`Config`
        """
        with open(config_file, "r") as f:
            self.object = yaml.load(f.read())
        self.object = self.get_from_keyring(self.object)
        self.set_attrs()

    def set_attrs(self):
        """
        Convert top level keys to attributes.

        Convenience function to allow cleaner code when
        referencing config values.
        """
        for k, v in self.object.items():
            setattr(self, k, v)

    def check_keyring(self, string):
        """
        Determine if value is in keyring, and if so, return it.

        Checks if the pattern matches the expected keyring reference style
        USE_KEYRING("name of keyring item"). If so, retrieves the proper
        value from the keyring and returns. otherwise, returns the string
        unmolested.

        keyring_app_name in the config file is used to determine the
        application name to be used for keyring lookup. This allows
        for certain convenience items, like sharing an LDAP password
        with other applications.

        :param string string: string to be checked.
        :rtype: string
        """
        app_name = self.object.get("keyring_app_name", "mssqlcli")
        match = self.matcher.match(string)
        if match is not None:
            return keyring.get_password(app_name, match.group(1))
        return string

    def get_from_keyring(self, obj):
        """
        Recursively scan Config for keyring values and retrieve them.

        :param dict obj: dictionary to be traversed.
        :returns: dict with all values retrieved from keyring.
        :rtype: dict
        """
        if type(obj) == list:
            iterable = enumerate(obj)
        if type(obj) == dict:
            iterable = obj.items()
        for k, v in iterable:
            if type(v) == str:
                obj[k] = self.check_keyring(v)
            if type(v) in [list, dict]:
                obj[k] = self.get_from_keyring(v)
        return obj

    def get_username(self):
        r"""
        Return domain\\username if using windows auth, otherwise username.

        Convenience function for abstracting windows authentication.
        """
        if self.object.get('windows_authentication', False):
            return '\\'.join([self.domain, self.username])
        return self.username
