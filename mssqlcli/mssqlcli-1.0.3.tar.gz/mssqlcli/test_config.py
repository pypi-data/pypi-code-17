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
# ---------------
# noqas:
# L28 - Exception will not be thrown on passing tests.

import mock

from mssqlcli import config


def simple_keyring(app_name, key):
    """Helper Function for Mocking a Keyring object."""
    if app_name != "mssqlcli_tests":
        raise Exception('keyring_app_name should be mssqlcli_tests')  # noqa
    if key == "username":
        return "a_user"
    if key == "password":
        return "a_password"
    if key == "a_list_item":
        return "secure_list_item"


def test_basic_config():
    """
    Test unmarshalling of a basic configuration file.

    Should contain plaintext username, password, and server strings.
    Config should apply these as attributes to itself.
    """
    c = config.Config('mssqlcli/test_fixtures/basic_config.yml')
    assert c.object == {
        "username": "a_user",
        "password": "a_password",
        'server': 'MY_MSSQL.example.com'
    }
    assert c.username == "a_user"
    assert c.password == "a_password"
    assert c.server == 'MY_MSSQL.example.com'


@mock.patch('keyring.get_password', side_effect=simple_keyring)
def test_config_keyring_support(mock_get_password):
    """
    Test the same basic config, but with retrieval of keyring items.

    username and password should be stored in the simple_keyring construct.
    """
    c = config.Config('mssqlcli/test_fixtures/basic_keyring_config.yml')
    assert c.object == {
        'keyring_app_name': 'mssqlcli_tests',
        "username": "a_user",
        "password": "a_password"
    }
    assert c.username == "a_user"
    assert c.password == "a_password"
    assert c.get_username() == "a_user"


@mock.patch('keyring.get_password', side_effect=simple_keyring)
def test_config_get_keyring_iteration(mock_get_password):
    """
    Test Nested keyring support.

    Tests that keyring item inside a list is retrieved.
    """
    c = config.Config('mssqlcli/test_fixtures/bogus_iterable_config.yml')
    assert c.object == {
        'keyring_app_name': 'mssqlcli_tests',
        'this_is_a_list': [
            "item_one",
            "item_two",
            "item_three",
            "secure_list_item"
        ]
    }


def test_config_windows_authentication():
    """Test that windows auth properly returns a formatted domain username."""
    c = config.Config('mssqlcli/test_fixtures/windows_auth_config.yml')
    assert c.get_username() == "MY_DOMAIN\\a_user"
