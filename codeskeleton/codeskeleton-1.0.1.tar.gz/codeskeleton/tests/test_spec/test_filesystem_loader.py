import os
import shutil
import tempfile
import unittest
from unittest import mock

import yaml

from codeskeleton import spec


class TestFilesystemLoader(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_directory)

    def mock_config(self, spec_directories):
        config = mock.MagicMock()
        config.spec_directories = spec_directories
        return config

    def make_spec_directory(self, root_directory, spec_type, spec_directory_name, spec_dict):
        spec_directory = os.path.join(self.temp_directory, root_directory,
                                      '{}s'.format(spec_type), spec_directory_name)
        os.makedirs(spec_directory)
        spec_file_path = os.path.join(spec_directory, 'codeskeleton.{}.yaml'.format(spec_type))
        with open(spec_file_path, 'w') as f:
            f.write(yaml.safe_dump(spec_dict))
            f.close()

    def test_find(self):
        self.make_spec_directory('root1', 'tree', 'spec1', {
            'id': 'spec1'
        })
        self.make_spec_directory('root2', 'tree', 'spec2', {
            'id': 'spec2'
        })
        self.make_spec_directory('root1', 'tree', 'spec3', {
            'id': 'spec3'
        })
        loader = spec.FileSystemLoader(
            config=self.mock_config([
                os.path.join(self.temp_directory, 'root1'),
                os.path.join(self.temp_directory, 'root2'),
            ]),
            spec_class=spec.Tree)
        specs = loader.find()
        ids = {specobject.id for specobject in specs}
        self.assertEqual(ids, {'spec1', 'spec2', 'spec3'})
