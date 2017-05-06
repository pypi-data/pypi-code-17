import re

_dependency_template = 'import {dep};\n'


def format_template(content):
    return remove_multiple_newlines(content)


def remove_multiple_newlines(content):
    return re.sub(r'(\n\n\n)+', r'\n', content)


def gen_dependency_string(fields):
    # Finds all the dependencies needed for the fields
    dependencies = ''
    for field in fields:
        if field.field_type.has_dependency() and field.field_type.dependency not in dependencies:
            dependencies += _dependency_template.format(
                dep=field.field_type.dependency)

    return dependencies
