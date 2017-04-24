import os
import tempfile
import unittest

import shutil

from codeskeleton import spec
from codeskeleton import template


class TestFile(unittest.TestCase):
    def setUp(self):
        self.enviroment_directory = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.enviroment_directory)

    def test_deserialize_empty_data(self):
        file = spec.File(path='mock')
        file.deserialize(data={})
        self.assertEqual(file.content, None)
        self.assertEqual(file.contentpath, None)
        self.assertEqual(file.template, None)
        self.assertEqual(file.templatepath, None)

    def test_deserialize_content(self):
        file = spec.File(path='mock')
        file.deserialize(data={'content': 'thecontent'})
        self.assertEqual(file.content, 'thecontent')
        self.assertEqual(file.contentpath, None)
        self.assertEqual(file.template, None)
        self.assertEqual(file.templatepath, None)

    def test_deserialize_contentpath(self):
        file = spec.File(path='mock')
        file.deserialize(data={'contentpath': 'the/content'})
        self.assertEqual(file.content, None)
        self.assertEqual(file.contentpath, 'the/content')
        self.assertEqual(file.template, None)
        self.assertEqual(file.templatepath, None)

    def test_deserialize_template(self):
        file = spec.File(path='mock')
        file.deserialize(data={'template': 'thetemplate'})
        self.assertEqual(file.content, None)
        self.assertEqual(file.contentpath, None)
        self.assertEqual(file.template, 'thetemplate')
        self.assertEqual(file.templatepath, None)

    def test_deserialize_templatepath(self):
        file = spec.File(path='mock')
        file.deserialize(data={'templatepath': 'the/template'})
        self.assertEqual(file.content, None)
        self.assertEqual(file.contentpath, None)
        self.assertEqual(file.template, None)
        self.assertEqual(file.templatepath, 'the/template')

    def test_get_output_path(self):
        file = spec.File(path='{{{testvariable1}}}/{{{testvariable2}}}')
        template_enviroment = template.make_environment(
            base_directory=self.enviroment_directory,
            variables={'testvariable1': 'a', 'testvariable2': 'b'})
        self.assertEqual(file.get_output_path(template_environment=template_enviroment),
                         'a/b')

    def test_get_content_content(self):
        file = spec.File(path='mock')
        file.deserialize(data={'content': 'thecontent'})
        template_enviroment = template.make_environment(
            base_directory=self.enviroment_directory, variables={})
        self.assertEqual(file.get_content(template_environment=template_enviroment),
                         'thecontent')

    def test_get_content_contentpath(self):
        file = spec.File(path='mock')
        file.deserialize(data={'contentpath': 'testfile.txt'})
        with open(os.path.join(self.enviroment_directory, 'testfile.txt'), 'w') as f:
            f.write('hello')
            f.close()
        template_enviroment = template.make_environment(
            base_directory=self.enviroment_directory, variables={})
        self.assertEqual(file.get_content(template_environment=template_enviroment),
                         'hello')

    def test_get_content_template(self):
        file = spec.File(path='mock')
        file.deserialize(data={'template': 'a = {{{ a }}}'})
        template_enviroment = template.make_environment(
            base_directory=self.enviroment_directory, variables={'a': 10})
        self.assertEqual(file.get_content(template_environment=template_enviroment),
                         'a = 10')

    def test_get_content_templatepath(self):
        file = spec.File(path='mock')
        file.deserialize(data={'templatepath': 'testfile.txt'})
        with open(os.path.join(self.enviroment_directory, 'testfile.txt'), 'w') as f:
            f.write('a = {{{ a }}}')
            f.close()
        template_enviroment = template.make_environment(
            base_directory=self.enviroment_directory, variables={'a': 10})
        self.assertEqual(file.get_content(template_environment=template_enviroment),
                         'a = 10')
