from collections import namedtuple
import platform
import unittest
from unittest.mock import Mock

from allinux import coreutils


class SystemContextTest(unittest.TestCase):
    def test_uname(self):
        Uname = namedtuple('Uname', ['system', 'node', 'release', 'version', 'machine', 'processor'])
        mocked_uname = Uname(
            system='Mocked Linux',
            node='Mocked node',
            release='Mocked release',
            version='Mocked version',
            machine='Mocked machine',
            processor='Mocked processor'
        )
        platform.uname = Mock(return_value=mocked_uname)
        
        self.assertEqual(coreutils.uname('-s').kernel_name, 'Mocked Linux')
        self.assertEqual(coreutils.uname('-r').kernel_release, 'Mocked release')
        