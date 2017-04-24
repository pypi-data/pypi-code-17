from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape


def make_environment(base_directory, variables):
    """
    Make a template environment.

    Changes block, variable and comment start/end strings to the following
    (mostly to make it easy to generate Django and jinja2 templates):

    - Blocks use ``{{% myblock %}}``.
    - Variables use ``{{{ myvariable }}}``.
    - Comments use ``{{# my comment #}}``.

    So just like the default jinja2 enviroment, with an extra ``{`` and ``}``.

    Args:
        base_directory: The base directory too lookup templates relative to.
        variables: Global variables to make available within the templates.

    Returns:
        jinja2.environment.Environment: The jinja2 template environment.
    """
    environment = Environment(
        autoescape=select_autoescape(['html', 'xml']),
        loader=FileSystemLoader(base_directory),
        block_start_string='{{%',
        block_end_string='%}}',
        variable_start_string='{{{',
        variable_end_string='}}}',
        comment_start_string='{{#',
        comment_end_string='#}}',
    )
    environment.globals.update(variables)
    return environment
