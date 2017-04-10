#!/usr/bin/env python3
# pylint: disable=wrong-import-position

"""Configuration tests"""

import os
import pickle

import pytest

from gtcms.core import ROOTPATH, hostname
from gtcms.core.Configuration import Configuration

_testDir = os.path.dirname(os.path.join(os.getcwd(), __file__))

PATH_IN = os.path.join(_testDir, 'config_in')

defaultContent = """
{
    "replace_me": {
        "__replace": "true",
        "this_has_been": "replaced"
    }
}
"""

expectedCfg = {
    'join_me': {
        'section_from_common': {
            'test': {
                'Client::ClientSessionInit': {
                    'class': 'Client',
                    'method': 'ClientSessionInit'
                }
            }
        },

        'from_module': {
            '20': {
                'GtLocale::init': {
                    'class': 'GtLocale',
                    'method': 'init'
                }
            }
        }
    },
    '__meta__': {
        'hostname': hostname(),
        'path': PATH_IN
    },
    'replace_me': {
        'this_has_been': 'replaced'
    },
    '__debug': 1,
    'donttouch': {
        'field1': '0',
        'a list': [8, 12, 24, 40, 80],
        'unquoted_number': 12,
        'classname': 'ExtendedClient',
        'text_bool': 'true'
    }
}


class TestConfiguration(object):

    """Configuration tests"""

    def test_property_custom(self):
        """Configuration.custom property pointing to file discovery test."""
        bc = Configuration(directory=PATH_IN)
        file = bc.custom
        expectedfile = os.path.join(PATH_IN, 'default.yml')
        assert str(file) == expectedfile

    def test_ParseDefaultHostConfig(self):
        """parse test"""
        bc = Configuration(directory=PATH_IN)
        ncfg = bc.get()
        assert ncfg

    def test_Loading(self):
        """Simple loading test for forced hostname from testing location."""
        bc = Configuration(directory=PATH_IN)
        ncfg = bc.get()
        assert ncfg == expectedCfg

    def test_default_path(self):
        """Test if default path is the same as expected one."""
        bc = Configuration()
        expected = ROOTPATH/'config'
        assert os.path.realpath(str(bc.path)) == str(expected)

    def test_other_cache_file(self):
        """Test if custom location of cache file is honored, by checking retrieved
        config against source cfg and doing the same with one got from pickle.load
        """
        bc = Configuration(directory=PATH_IN, cache='caches/test.pickle')
        cfg1 = bc.get()
        with open(str(ROOTPATH/'caches/test.pickle'), 'rb') as fh:
            cfg2 = pickle.load(fh)
        os.unlink(str(ROOTPATH/'caches/test.pickle'))
        assert expectedCfg == cfg1
        assert expectedCfg == cfg2

    def test_init_directory_and_cache(self):
        """Test if basePath parameter is honored."""
        bc = Configuration(directory=PATH_IN, cache='caches/test.pickle')
        cfg = bc.get()
        os.unlink(str(ROOTPATH / 'caches/test.pickle'))
        assert cfg == expectedCfg

    def testGetString(self):
        """Test fetching string from known path."""
        bc = Configuration(directory=PATH_IN)
        assert bc.get('replace_me', 'this_has_been') == 'replaced'

    def testGetDefault(self):
        """Test fetching default for not existing entry."""
        bc = Configuration(directory=PATH_IN)
        assert bc.get('replace_me', 'this_doesnt_exist', default='testcase') == 'testcase'

    def testGetDict(self):
        """Test fetching whole dict from known path."""
        bc = Configuration(directory=PATH_IN)
        assert bc.get('replace_me') == {'this_has_been': 'replaced'}

    def testGetList(self):
        """Test fetching list from known path."""
        bc = Configuration(directory=PATH_IN)
        assert bc.get('donttouch', 'a list') == [8, 12, 24, 40, 80]

    def testGetNotFound(self):
        """Test exception for not found entry."""
        bc = Configuration(directory=PATH_IN)
        with pytest.raises(KeyError):
            bc.get('nonexistent', 'path')
