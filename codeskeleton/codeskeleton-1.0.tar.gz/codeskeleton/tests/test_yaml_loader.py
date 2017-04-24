import textwrap
import unittest
from collections import OrderedDict

import yaml

from codeskeleton import yaml_loader


class TestOrderedDictYAMLLoader(unittest.TestCase):
    def test_loads_mappings_as_ordered_dict(self):
        data = yaml.load(
            textwrap.dedent("""
            a: 10
            b: 20
            c: 30"""),
            Loader=yaml_loader.OrderedDictSafeLoader)
        self.assertEqual(data, OrderedDict([
            ('a', 10),
            ('b', 20),
            ('c', 30),
        ]))
