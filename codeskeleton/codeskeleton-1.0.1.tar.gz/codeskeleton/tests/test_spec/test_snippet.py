import shutil
import tempfile
import unittest
from collections import OrderedDict

from codeskeleton import exceptions
from codeskeleton import spec
from codeskeleton import template


class TestSnippet(unittest.TestCase):
    def setUp(self):
        self.enviroment_directory = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.enviroment_directory)

    def test_deserialize_empty_data(self):
        snippet = spec.Snippet(base_directory=self.enviroment_directory)
        snippet.deserialize(data={})
        self.assertEqual(snippet.id, None)
        self.assertEqual(snippet.title, None)
        self.assertEqual(snippet.description, None)
        self.assertEqual(len(snippet.variables), 0)
        self.assertEqual(snippet.template, None)
        self.assertEqual(snippet.templatepath, None)

    def test_deserialize_with_data(self):
        snippet = spec.Snippet(base_directory=self.enviroment_directory)
        snippet.deserialize(data={
            'id': 'mockid',
            'title': 'thetitle',
            'description': 'thedescription',
            'variables': OrderedDict([
                ('testvariable1', {}),
                ('testvariable2', {})
            ]),
            'template': 'test',
            'templatepath': 'test.codeskeleton.txt',
        })
        self.assertEqual(snippet.id, 'mockid')
        self.assertEqual(snippet.title, 'thetitle')
        self.assertEqual(snippet.description, 'thedescription')
        self.assertEqual(len(snippet.variables), 2)
        self.assertEqual(snippet.variables.get_variable('testvariable1').name, 'testvariable1')
        self.assertEqual(snippet.variables.get_variable('testvariable2').name, 'testvariable2')
        self.assertEqual(snippet.template, 'test')
        self.assertEqual(snippet.templatepath, 'test.codeskeleton.txt')

    def test_get_content_from_template(self):
        snippet = spec.Snippet(base_directory=self.enviroment_directory,
                               template='a = {{{ a }}}',
                               variables=spec.Variables(
                                   spec.Variable(name='a', value=10)
                               ))

        self.assertEqual(snippet.render(), 'a = 10')

    def __make_kwargs(self, **overrides):
        overrides.setdefault('base_directory', self.enviroment_directory)
        overrides.setdefault('context', 'mockcontext')
        overrides.setdefault('id', 'mockid')
        overrides.setdefault('template', 'mocktemplate')
        return overrides

    def test_validate_spec_no_id(self):
        snippet = spec.Snippet(**self.__make_kwargs(id=None))
        with self.assertRaisesRegex(exceptions.SpecValidationError,
                                    '^id: This attribute is required.$'):
            snippet.validate_spec()

    def test_validate_spec_no_context(self):
        snippet = spec.Snippet(**self.__make_kwargs(context=None))
        with self.assertRaisesRegex(exceptions.SpecValidationError,
                                    '^context: This attribute is required.$'):
            snippet.validate_spec()

    def test_validate_spec_invalid_context(self):
        snippet = spec.Snippet(**self.__make_kwargs(context='two words'))
        with self.assertRaisesRegex(exceptions.SpecValidationError,
                                    '^context: Must be a lowercase single word containing only a-z and numbers.$'):
            snippet.validate_spec()

    def test_validate_spec_no_template(self):
        snippet = spec.Snippet(**self.__make_kwargs(template=None, templatepath=''))
        with self.assertRaisesRegex(exceptions.SpecValidationError,
                                    '^template|templatepath: "template" or "templatepath" is required$'):
            snippet.validate_spec()
