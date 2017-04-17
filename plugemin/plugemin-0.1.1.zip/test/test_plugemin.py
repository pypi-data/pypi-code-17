import os
import io
import plugemin
import unittest

try:
    from unittest import mock
except ImportError:
    import mock


class Loader(object):
    def __init__(self, name, obj):
        self.obj = obj
        self.name = name

    def load(self):
        return self.obj


csv = [
    "name,age,gender\n",
    "alice,23,female\n",
    "bob,32,male\n",
]

json = [
"""{
    "name": "alice",
    "age": 23,
    "gender": "female"
}""",
"""{
    "name": "bob",
    "age": 32,
    "gender": "male"
}"""]

xml = [
"""<root>
    <name>alice</name>
    <age>23</age>
    <gender>female</gender>
</root>""",
"""<root>
    <name>bob</name>
    <age>32</age>
    <gender>male</gender>
</root>""",
]

template = """Hello {{name}}, \nI understand that you are a {{gender}} of {{age}} years of age."""

inmem_file = io.StringIO()

def join_with_expanduser(path):
    return os.path.abspath(os.path.expanduser(os.path.join(*path)))


class TestPlugemin(unittest.TestCase):
    @mock.patch("pkg_resources.iter_entry_points", return_value=[Loader("CsvInput", plugemin.CsvInput), Loader("JsonInput", plugemin.JsonInput)])
    def test_plugemin_template(self, mock_entrypoints):
        """plugemin should take a series of structured data
        and render templates based on each item in the input.

        By default, the template is rendered as a jinja2 template
        and we accept csv
        """
        results = list(plugemin.render(template, csv))
        expected = [
            """Hello alice, \nI understand that you are a female of 23 years of age.""",
            """Hello bob, \nI understand that you are a male of 32 years of age.""",
        ]
        self.assertEqual(expected, results)

    @mock.patch("os.path.isdir", return_value=False)
    @mock.patch("pkg_resources.iter_entry_points", return_value=[Loader("CsvInput", plugemin.CsvInput), Loader("JsonInput", plugemin.JsonInput)])
    def test_plugemin_template_search_path(self, mock_entrypoints, mock_isdir):
        results = list(plugemin.render(template, csv))
        calls = [
            mock.call(join_with_expanduser(["/", "plugemin", "templates"])),
            mock.call(join_with_expanduser(["~", "plugemin", "templates"])),
            mock.call(join_with_expanduser([".", "plugemin", "templates"])),
        ]
        mock_isdir.assert_has_calls(calls)


class TestInputPlugins(unittest.TestCase):

    @mock.patch("pkg_resources.iter_entry_points", return_value=[Loader("CsvInput", plugemin.CsvInput), Loader("JsonInput", plugemin.JsonInput)])
    def test_CsvInput_plugin(self, mock_entrypoints):
        """an input plugin is designed to take an iterator and
        yield dicts based on each item yielded.
        """
        results = list(plugemin.render(template, csv, input_plugin="CsvInput"))
        expected = [
            """Hello alice, \nI understand that you are a female of 23 years of age.""",
            """Hello bob, \nI understand that you are a male of 32 years of age.""",
        ]
        self.assertEqual(expected, results)

    @mock.patch("pkg_resources.iter_entry_points", return_value=[Loader("CsvInput", plugemin.CsvInput), Loader("JsonInput", plugemin.JsonInput)])
    def test_JsonInput_plugin(self, mock_entrypoints):
        results = list(plugemin.render(template, json, input_plugin="JsonInput"))
        expected = [
            """Hello alice, \nI understand that you are a female of 23 years of age.""",
            """Hello bob, \nI understand that you are a male of 32 years of age.""",
        ]
        self.assertEqual(expected, results)

    @mock.patch("pkg_resources.iter_entry_points", return_value=[Loader("CsvInput", plugemin.CsvInput), Loader("JsonInput", plugemin.JsonInput), Loader("XmlInput", plugemin.XmlInput)])
    def test_XmlInput_plugin(self, mock_entrypoints):
        results = list(plugemin.render(template, xml, input_plugin="XmlInput"))
        expected = [
            """Hello alice, \nI understand that you are a female of 23 years of age.""",
            """Hello bob, \nI understand that you are a male of 32 years of age.""",
        ]
        self.assertEqual(expected, results)

    @mock.patch("pkg_resources.iter_entry_points", return_value=[Loader("CsvInput", plugemin.CsvInput)])
    def test_find_plugins_calls_pkgutils_iter_entry_points(self, mock_entrypoints):
        with self.assertRaises(KeyError):
            results = list(plugemin.render(template, json, input_plugin="JsonInput"))
