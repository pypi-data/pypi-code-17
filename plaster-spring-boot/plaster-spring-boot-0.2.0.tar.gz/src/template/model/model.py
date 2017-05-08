import re

import src.data.regex as regices
import src.data.settings as settings
import src.template.template_util as template_util
from current import TEMPLATE as TEMPLATE
from current_lombok import TEMPLATE as LOMBOK_TEMPLATE

_field_template = '''
    private {type} {name};
'''

_getter_setter_template = '''
    public {type} get{cap_name}() {{
        return this.{name};
    }}

    public void set{cap_name}({type} {name}) {{
        this.{name} = {name};
    }}
'''


def get_template(enable_lombok):
    return LOMBOK_TEMPLATE if enable_lombok else TEMPLATE


def gen_contents(file_info):
    fields = [settings.ID] + file_info.fields
    body = ''

    # Enters all the fields to be associated with the model
    for field in file_info.fields:
        body += _field_template.format(type=field.field_type.class_name, name=field.name)

    dependencies = template_util.gen_dependency_string(fields)

    # If lombok is not supported, we must manually
    # enter in the getters and the setters
    if not settings.IS_LOMBOK_SUPPORTED:
        for field in fields:
            body += _getter_setter_template.format(
                type=field.field_type.class_name,
                name=field.name,
                cap_name=field.name[0].upper() + field.name[1:])

    return template_util.format_template(get_template(settings.IS_LOMBOK_SUPPORTED).format(
        package=file_info.package,
        dependencies=dependencies,
        class_name=file_info.class_name,
        id=settings.ID,
        header='',
        body=body))


def alter_contents(file_info):
    existing_file = open(file_info.file_path + file_info.file_name)
    if not existing_file:
        raise IOError('Cannot add field(s) to ' + file_info.file_name + ' - File does not exist')

    body_since_last_var_match = ''
    body_to_last_var_match = body_since_last_var_match

    # This iterates through the file and finds the end of field
    # declarations at the top of the file. When it finds the end,
    # it appends the field declaration(s) for the new field(s)
    for line in existing_file:
        body_since_last_var_match += line
        reg_results = re.search(regices.VARIABLE_DECLARATION, line)
        if reg_results:
            # Makes sure the variable name isn't already taken
            var_name = reg_results.group(3) + reg_results.group(4)
            for field in file_info.fields:
                if field.name == var_name:
                    raise Exception('Cannot add field [\'%s\'] - already exists for model \'%s\'' % (
                        field.name, file_info.class_name))

            body_to_last_var_match += body_since_last_var_match
            body_since_last_var_match = ''
        elif re.match(regices.METHOD, line):
            # This means we should inject the variable declaration in
            # between body_to_last_var_match and body_since_last_var_match
            for field in file_info.fields:
                body_to_last_var_match += _field_template.format(type=field.field_type.class_name, name=field.name)
            break

    body = body_to_last_var_match + body_since_last_var_match

    for line in existing_file:
        if settings.IS_LOMBOK_SUPPORTED or not re.match(regices.END_OF_FILE, line):
            body += line
        else:
            # Add the getters and setters for the fields
            for field in file_info.fields:
                body += _getter_setter_template.format(
                    type=field.field_type.class_name,
                    name=field.name,
                    cap_name=field.name[0].upper() + field.name[1:])

                body += '}\n'

    return body
