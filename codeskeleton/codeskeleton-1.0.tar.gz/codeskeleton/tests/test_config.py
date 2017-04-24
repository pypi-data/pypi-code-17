import os
import tempfile
import textwrap
import unittest

import shutil

from codeskeleton.config import Config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config_directory = tempfile.mkdtemp()
        self.config_path = os.path.join(self.config_directory, 'config.yaml')

    def tearDown(self):
        shutil.rmtree(self.config_directory)

    def test_register_spec_directory(self):
        config = Config(path=self.config_path)
        config.register_spec_directory('/test')
        self.assertEqual(
            config.spec_directories,
            {'/test'})

    def test_unregister_spec_directory(self):
        config = Config(path=self.config_path)
        config.spec_directories = {'/test'}
        config.unregister_spec_directory('/test')
        self.assertEqual(
            config.spec_directories,
            set())

    def test_has_spec_directory(self):
        config = Config(path=self.config_path)
        config.spec_directories = {'/test'}
        self.assertTrue(config.has_spec_directory('/test'))
        self.assertFalse(config.has_spec_directory('/test2'))

    def test_update_from_dict(self):
        config = Config(path=self.config_path)
        config.update_from_dict({
            'spec_directories': [
                '/test1',
                '/test2'
            ]
        })
        self.assertEqual(config.spec_directories,
                         {'/test1', '/test2'})

    def test_serialize(self):
        config = Config(path=self.config_path)
        config.spec_directories = {'/test1', '/test2'}
        serialized = config.serialize()
        self.assertEqual(serialized['spec_directories'], [
            '/test1',
            '/test2'
        ])

    def test_load_from_disk(self):
        open(self.config_path, 'w').write(textwrap.dedent("""
        spec_directories:
        - /test1
        - /test2
        """))
        config = Config(path=self.config_path)
        config.load_from_disk()
        self.assertEqual(
            config.spec_directories,
            {'/test1', '/test2'})

    def test_save_to_disk(self):
        config = Config(path=self.config_path)
        config.register_spec_directory('/test1')
        config.register_spec_directory('/test2')
        config.save_to_disk()
        filecontent = open(self.config_path, 'r').read()
        self.assertEqual(
            filecontent,
            'spec_directories:\n'
            '- /test1\n'
            '- /test2\n')
