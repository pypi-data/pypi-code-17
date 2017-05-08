import os
import re


def create_file(path, name, file_contents, create_not_found_dirs=True, mode="w+"):
    if create_not_found_dirs and not os.path.isdir(path):
        os.makedirs(path)

    new_file = open(os.path.join(path, name), mode)
    new_file.write(file_contents)
    new_file.close()


def type_to_var(java_type):
    return java_type[0].lower() + java_type[1:]


def type_to_snake_case(java_type):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', java_type)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def search_for_filename(path, lowercase_name):
    """
    Searches for the given filename. Will to an ignore-case
    comparison.

    :param path: path to folder to start search
    :param lowercase_name: name of file to find
    :return: list of files that match the name
    """
    result = []
    for root, dirs, files in os.walk(path):
        for filename in files:
            if lowercase_name == filename.lower():
                result.append(os.path.join(root, filename))
    return result

