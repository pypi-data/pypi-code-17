import pkg_resources
import jinja2
import json
import csv
import io
import os

__all__ = [
    "find_input_plugins",
    "find_templates",
    "render",
]
def _join_with_expanduser(path):
    return os.path.abspath(os.path.expanduser(os.path.join(*path)))


def find_input_plugins():
    """Return a dict containing installed plugins keyed by name
    with the value being the actual plugin class.

    :returns: A dict containing all installed plugins
    :rtype: dict
    """
    plugins = {}
    for plugin in pkg_resources.iter_entry_points("plugemin.InputPlugin"):
        plugins[plugin.name] = plugin.load()
    return plugins

def find_templates():
    """Finds all available templates, returns a dict with the filename
    as the keys pointing to the file contents.

    Looks in ``/plugemin/templates``, ``~/plugemin/templates`` and
    ``./plugemin/templates``

    :returns: A dict containing all available templates
    :rtype: dict
    """
    _templates = {}
    paths = [
        _join_with_expanduser(["/", "plugemin", "templates"]),
        _join_with_expanduser(["~", "plugemin", "templates"]),
        _join_with_expanduser([".", "plugemin", "templates"]),
    ]
    for path in paths:
        if os.path.isdir(path):
            _templates.update({
                filename: os.path.join(path, filename)
                for filename in os.listdir(path)})
    return _templates

def render(_template, data, input_plugin=None):
    """Render ``_template`` for each row in ``data`` using ``input_plugin``
    to parse the incoming data.

    :param _template: A str containing the name of the template to render
    :data: An iterator yielding discrete pieces of information parsed by input_plugin
    :param input_plugin: the input plugin to use, defaults to CsvInput
    :type _template: str
    :type data: iterator
    :type input_plugin: class
    """
    input_plugins = find_input_plugins()
    _templates = find_templates()
    if _template in _templates.keys():
        with open(_templates[_template], "r") as fp:
            _template = fp.read()
    if input_plugin is None:
        input_plugin = "CsvInput"
    if isinstance(input_plugin, str):
        input_plugin = input_plugins[input_plugin]

    _template = jinja2.Template(_template)
    for row in input_plugin(data):
        yield _template.render(**row)
