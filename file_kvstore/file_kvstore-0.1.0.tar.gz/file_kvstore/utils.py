from contextlib import contextmanager

from .constants import DEFAULT_FILE
from .io import get_dict_from_yaml
from .io import write_dict_to_yaml


@contextmanager
def modify_yaml_dictionary(filename=DEFAULT_FILE):
    try:
        dictionary = get_dict_from_yaml(filename)
        yield dictionary
    finally:
        write_dict_to_yaml(filename, dictionary)


def update(key, value, filename=DEFAULT_FILE):
    with modify_yaml_dictionary(filename) as obj:
        obj[key] = value
