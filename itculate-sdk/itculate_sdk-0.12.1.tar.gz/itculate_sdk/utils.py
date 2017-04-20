#
# (C) ITculate, Inc. 2015-2017
# All rights reserved
# Licensed under MIT License (see LICENSE)
#
import os
import yaml

from .mappings import clear_mappings
from .mappings import add_statsd_mapping_rule


class ReadOnlyDict(dict):
    def __init__(self, dict_to_protect=None):
        super(ReadOnlyDict, self).__init__(dict_to_protect)

    def __setitem__(self, key, value):
        raise TypeError("__setitem__ is not permitted")

    def __delitem__(self, key):
        raise TypeError("__delitem__ is not permitted")

    def update(self, other=None, **kwargs):
        raise TypeError("update is not permitted")


def check_keys(keys):
    """
    Given a dict of keys, make sure they follow the required pattern and constraints

    :param dict[str, str] keys: Set of keys to check
    """
    assert keys and isinstance(keys, dict) and len(keys) > 0, "Keys are mandatory (non empty dict)"

    # Make sure values are unique
    assert len(set(keys.viewvalues())) == len(keys), "Same value for more than one key"


def load_mapping_rules(file_path):
    assert os.path.exists(file_path), "File {} does not exist".format(file_path)

    with open(file_path, "r") as f:
        # Based on the content-type, parse the payload
        list_of_rules = yaml.load(f)

        itsdk_data_types_module = __import__("itculate_sdk.types")

        # Clear previous mappings
        clear_mappings()

        # Load the new ones
        for rule in list_of_rules:
            # Dynamically load the data type form name
            data_type_class_name = "{}DataType".format(rule["data_type"])
            data_type_class = getattr(itsdk_data_types_module, data_type_class_name)
            data_type = data_type_class()

            # Update the SDK with this mapping
            add_statsd_mapping_rule(statsd_host_pattern=rule["statsd_host_pattern"],
                                    statsd_counter_pattern=rule["statsd_counter_pattern"],
                                    statsd_tags_patterns=rule["statsd_tags_patterns"],
                                    instance_id_pattern=rule["instance_id_pattern"],
                                    vertex_key_template=rule["vertex_key_template"],
                                    counter_template=rule["counter_template"],
                                    data_type=data_type)
