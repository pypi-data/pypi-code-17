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


def insert_dependencies(existing_file, file_info):
    """
    Inserts the required dependencies into the file for the given information

    :param existing_file: file to insert in to
    :param file_info: information about the content to be generated
    :return: the content written
    """
    fields_with_dependencies = [field for field in file_info.fields if field.field_type.has_dependency()]

    content_to_last_dependency = ""
    content_from_last_dependency = ""
    for line in existing_file:
        content_from_last_dependency += line
        reg_results = re.search(regices.IMPORT_DECLARATION, line)
        if reg_results:
            dependency = reg_results.group(2)
            for field in fields_with_dependencies:
                if field.field_type.dependency == dependency:
                    fields_with_dependencies.remove(field)
            content_to_last_dependency += content_from_last_dependency
            content_from_last_dependency = ""
        elif re.match(regices.CLASS, line):
            # This means we've reached the class declaration
            # and should therefore have injected the imports
            # after the last dependency that we saw.
            content_to_last_dependency += template_util.gen_dependency_string(fields_with_dependencies)
            break

    return content_to_last_dependency + content_from_last_dependency


def insert_fields(existing_file, content_string, file_info):
    """
    Inserts the required field declarations into the file for the given information

    :param existing_file: file to insert in to
    :param content_string: file we are building, the string to add to
    :param file_info: information about the content to be generated
    :return: the content written
    """
    body_to_last_var_match = content_string
    body_from_last_var_match = ''

    # This iterates through the file and finds the end of field
    # declarations at the top of the file. When it finds the end,
    # it appends the field declaration(s) for the new field(s)
    for line in existing_file:
        body_from_last_var_match += line

        variable_match = re.search(regices.VARIABLE_DECLARATION, line)
        method_match = re.search(regices.METHOD, line)
        eof_match = re.search(regices.END_OF_FILE, line)
        if variable_match:
            # Makes sure the variable name isn't already taken
            var_name = variable_match.group(3) + variable_match.group(4)
            for field in file_info.fields:
                if field.name == var_name:
                    raise Exception('Cannot add field [\'%s\'] - already exists for model \'%s\'' % (
                        field.name, file_info.class_name))

            body_to_last_var_match += body_from_last_var_match
            body_from_last_var_match = ''
        elif method_match or eof_match:
            # This means we should inject the variable declaration in
            # between body_to_last_var_match and body_since_last_var_match
            for field in file_info.fields:
                body_to_last_var_match += _field_template.format(type=field.field_type.class_name, name=field.name)

            if eof_match:
                body_to_last_var_match = inject_getters_and_setters(body_to_last_var_match, file_info)
            break

    return body_to_last_var_match + body_from_last_var_match


def inject_getters_and_setters(content_string, file_info):
    """
    Inserts the necessary method declarations for getters and setters,
    if we are not using lombok

    :param content_string: file we are building, the string to add to
    :param file_info: information about the content to be generated
    :return: the content written
    """
    if not settings.IS_LOMBOK_SUPPORTED:
        # Add the getters and setters for the fields
        for field in file_info.fields:
            content_string += _getter_setter_template.format(
                type=field.field_type.class_name,
                name=field.name,
                cap_name=field.name[0].upper() + field.name[1:])

    return content_string


def insert_getters_and_setters(existing_file, content_string, file_info):
    """
    Iterates to the end of the file and inserts the required method
    declarations for getters and setters into the file for the given information

    :param existing_file: file to insert in to
    :param content_string: file we are building, the string to add to
    :param file_info: information about the content to be generated
    :return: the content written
    """
    for line in existing_file:
        if settings.IS_LOMBOK_SUPPORTED or not re.match(regices.END_OF_FILE, line):
            content_string += line
        else:
            content_string = inject_getters_and_setters(content_string, file_info)

    return content_string


def alter_contents(file_info):
    """
    Adds the fields found within the file information to the file defined by the file_info.
    This will insert the following things:

        1 - Any needed dependencies (imports) that are needed for the new fields.
            These will only be injected if the dependency is not already satisfied
        2 - Any needed fields that are needed. If the field name is already taken,
            will throw an error to prevent further generation
        3 - Any methods needed (getters/setters). This will only happen if Lombok
            is not supported

    :param file_info: information definining the file and how to alter it
    :return: the altered file's contents
    """
    existing_file = open(file_info.file_path + file_info.file_name)
    if not existing_file:
        raise IOError('Cannot add field(s) to ' + file_info.file_name + ' - File does not exist')

    content_string = insert_dependencies(existing_file, file_info)
    content_string = insert_fields(existing_file, content_string, file_info)
    content_string = insert_getters_and_setters(existing_file, content_string, file_info)

    return content_string
