import os
import shutil
import tempfile
import unittest
from collections import OrderedDict

from codeskeleton import exceptions
from codeskeleton import spec


class TestTree(unittest.TestCase):
    def setUp(self):
        self.enviroment_directory = tempfile.mkdtemp()
        self.output_directory = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.enviroment_directory)
        shutil.rmtree(self.output_directory)

    def test_deserialize_empty_data(self):
        tree = spec.Tree(base_directory=self.enviroment_directory)
        tree.deserialize(data={})
        self.assertEqual(tree.id, None)
        self.assertEqual(tree.title, None)
        self.assertEqual(tree.description, None)
        self.assertEqual(len(tree.variables), 0)
        self.assertEqual(len(tree.files), 0)

    def test_deserialize_with_data(self):
        tree = spec.Tree(base_directory=self.enviroment_directory)
        tree.deserialize(data={
            'id': 'mockid',
            'title': 'thetitle',
            'description': 'thedescription',
            'files': OrderedDict([
                ('a', {'content': '1'}),
                ('b', {'content': '2'}),
            ]),
            'variables': OrderedDict([
                ('testvariable1', {}),
                ('testvariable2', {})
            ])
        })
        self.assertEqual(tree.id, 'mockid')
        self.assertEqual(tree.title, 'thetitle')
        self.assertEqual(tree.description, 'thedescription')
        self.assertEqual(len(tree.variables), 2)
        self.assertEqual(tree.variables.get_variable('testvariable1').name, 'testvariable1')
        self.assertEqual(tree.variables.get_variable('testvariable2').name, 'testvariable2')
        self.assertEqual(len(tree.files), 2)
        self.assertEqual(tree.files._files[0].path, 'a')
        self.assertEqual(tree.files._files[1].path, 'b')

    def test_collect_writers_overwrite_false(self):
        tree = spec.Tree(base_directory=self.enviroment_directory)
        tree.files.add_files(
            spec.File(path='a.txt', content='acontent'),
            spec.File(path='b.txt', content='bcontent'),
        )
        with open(os.path.join(self.output_directory, 'a.txt'), 'w') as f:
            f.write('x')
        skipped_writers, writers = tree.collect_writers(output_directory=self.output_directory)
        self.assertEqual(len(skipped_writers), 1)
        self.assertEqual(skipped_writers[0].file.path, 'a.txt')
        self.assertEqual(len(writers), 1)
        self.assertEqual(writers[0].file.path, 'b.txt')

    def test_collect_writers_overwrite_true(self):
        tree = spec.Tree(base_directory=self.enviroment_directory)
        tree.files.add_files(
            spec.File(path='a.txt', content='acontent'),
            spec.File(path='b.txt', content='bcontent'),
        )
        with open(os.path.join(self.output_directory, 'a.txt'), 'w') as f:
            f.write('x')
        skipped_writers, writers = tree.collect_writers(output_directory=self.output_directory,
                                                        overwrite=True)
        self.assertEqual(len(skipped_writers), 0)
        self.assertEqual(len(writers), 2)
        self.assertEqual(writers[0].file.path, 'a.txt')
        self.assertEqual(writers[1].file.path, 'b.txt')

    def __make_kwargs(self, **overrides):
        overrides.setdefault('base_directory', self.enviroment_directory)
        overrides.setdefault('id', 'mockid')
        return overrides

    def test_validate_spec_no_id(self):
        tree = spec.Tree(**self.__make_kwargs(id=None))
        with self.assertRaisesRegex(exceptions.SpecValidationError,
                                    '^id: This attribute is required.$'):
            tree.validate_spec()

    def test_validate_spec_no_context(self):
        tree = spec.Tree(**self.__make_kwargs(context=None))
        with self.assertRaisesRegex(exceptions.SpecValidationError,
                                    '^context: This attribute is required.$'):
            tree.validate_spec()

    def test_validate_spec_invalid_context(self):
        tree = spec.Tree(**self.__make_kwargs(context='two words'))
        with self.assertRaisesRegex(exceptions.SpecValidationError,
                                    '^context: Must be a lowercase single word containing only a-z and numbers.$'):
            tree.validate_spec()
