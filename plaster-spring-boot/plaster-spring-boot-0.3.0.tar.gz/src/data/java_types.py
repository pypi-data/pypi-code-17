import os

import settings as settings
import src.util.util as util

INT_PRIM = 'int'
LONG_PRIM = 'long'
DOUBLE_PRIM = 'double'
FLOAT_PRIM = 'float'
BYTE_PRIM = 'byte'
BOOLEAN_PRIM = 'boolean'

STRING = 'String'
INTEGER = 'Integer'
LONG = 'Long'
DOUBLE = 'Double'
FLOAT = 'Float'
BYTE = 'Byte'
BOOLEAN = 'Boolean'

DATE = 'Date'
TIMESTAMP = 'Timestamp'

java_types = {
    'string': STRING,
    'str': STRING,
    'int': INTEGER,
    'integer': INTEGER,
    'long': LONG,
    'date': DATE,
    'timestamp': TIMESTAMP,
}

dependencies = {
    DATE: 'java.util.Date',
    TIMESTAMP: 'java.sql.Timestamp'
}


def fetch_type(type_string):
    """
    Fetches the type related to the given type.
    For example "int" -> "integer" and so forth.

    This also allows to find objects that are defined in
    the project. For example "Person" will go to the "Person"
    object if a "Person.java" file is found.

    :param type_string: string representing the type
    :return: the java type
    """
    key = type_string.lower()
    return java_types[key] if key in java_types else __fetch_custom_type(type_string)


def fetch_dependency(java_type):
    """
    Fetches the dependency of the given java_type. For example
    "Date" needs to be imported and "java.util.Date" will be returned

    :param java_type: type of java object to find a dependency for
    :return: the dependency to be used as an import
    """
    return dependencies[java_type] if java_type in dependencies else __fetch_custom_dependency(java_type)


def __fetch_custom_type(type_string):
    """
    Will search the repository for any classes matching the string.
    So if "person" is the argument and a "Person.java" class is
    found, it will return that. If multiple are found, will return all.

    :param type_string: string representing the type
    :return: the java type
    """
    files = util.search_for_filename(settings.BASE_PATH, type_string.lower() + ".java")
    if len(files) == 0:
        return None
    elif len(files) == 1:
        # src/main/.../something.java -> something
        return os.path.basename(files[0]).split(".")[0]
    else:
        raise Exception("Could not determine which " + type_string + " to use. Options: " + files)


def __fetch_custom_dependency(type_string):
    """
    Will search the repository for any classes matching the string.
    So if "person" is the argument and a "Person.java" class is
    found, it will return that. If multiple are found, will return all.

    :param type_string: string representing the type
    :return: the java type
    """
    files = util.search_for_filename(settings.BASE_PATH, type_string.lower() + ".java")
    if len(files) == 0:
        return None
    elif len(files) == 1:
        # src/main/java/package/something.java -> package.something.java
        return files[0].split("java")[1][1:].replace("/", ".").replace("\\", ".")[:-1]
    else:
        raise Exception("Could not determine which " + type_string + " to use. Options: " + files)
