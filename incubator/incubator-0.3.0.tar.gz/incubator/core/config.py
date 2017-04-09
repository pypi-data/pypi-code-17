"""
Class for managing configuration.
"""

import jsonschema
import six

from .constants import (CONFIG_BUILDARGS, CONFIG_CONTAINER_LIMITS,
                        CONFIG_CONTEXT_FILE_LIMIT, CONFIG_INFINITE_COMMAND,
                        CONFIG_LABELS, CONFIG_LAYERS, CONFIG_MKDIR_COMMAND,
                        CONFIG_PULL, CONFIG_TAGS, CONFIG_VERSION,
                        CONFIG_VOLUMES, DEFAULT_CONTEXT_FILE_LIMIT,
                        DEFAULT_TAG, DEFAULT_VERSION, INFINITE_COMMAND,
                        MKDIR_COMMAND)
from .utils import volumes_to_dict

schema_v1 = {
    "type": "object",
    "properties": {
        CONFIG_VERSION: {"type": "number"},
        CONFIG_LAYERS: {
            "type": "array",
            "items": {
                "type": "integer",
                "minimum": 1
            },
        },
        CONFIG_VOLUMES: {
            "properties": {},
            "patternProperties": {
                "": {
                    "type": "string"
                }
            }
        },
        CONFIG_LABELS: {
            "properties": {},
            "patternProperties": {
                "": {
                    "type": "string"
                }
            }
        },
        CONFIG_INFINITE_COMMAND: {"type": "string"},
        CONFIG_MKDIR_COMMAND: {'type': 'string'},
        CONFIG_CONTEXT_FILE_LIMIT: {'type': 'integer'},
        CONFIG_TAGS: {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    },
}

schema = {1.0: schema_v1}


class ImageConfig(object):
    """
    Representation of config file.
    Structure of file is described and validated by jsonschema.
    """

    def __init__(self, config_dict=None, pull=False,
                 rm=False, forcerm=False, buildargs=None,
                 container_limits=None, labels=None,
                 layers=None, tag=None,
                 secret_volumes=None,
                 infinite_command=None,
                 mkdir_command=None,
                 context_file_limit=None,
                 ):

        config_dict = config_dict or {}
        config_dict.setdefault(CONFIG_VERSION, DEFAULT_VERSION)
        self.__config = config_dict

        self._update_dict(CONFIG_BUILDARGS, buildargs)
        self._update_dict(CONFIG_CONTAINER_LIMITS, container_limits)
        self._update_dict(CONFIG_VOLUMES, volumes_to_dict(secret_volumes))
        self._update_dict(CONFIG_LABELS, labels)

        self._update_value(CONFIG_CONTEXT_FILE_LIMIT, context_file_limit, DEFAULT_CONTEXT_FILE_LIMIT)
        self._update_value(CONFIG_PULL, pull, False)

        self._update_sorted_array(CONFIG_LAYERS, layers)

        self._update_sorted_array(CONFIG_TAGS, tag)

        self._update_value(CONFIG_INFINITE_COMMAND, infinite_command, INFINITE_COMMAND)
        self._update_value(CONFIG_MKDIR_COMMAND, mkdir_command, MKDIR_COMMAND)

    def _update_dict(self, key, value):
        value = value or {}
        self.__config.setdefault(key, {})
        self.__config[key].update(value)

    def _update_sorted_array(self, key, value):
        value = value or []
        if isinstance(value, six.string_types):
            value = [value]
        self.__config.setdefault(key, [])
        self.__config[key] = list(set(self.__config[key] + value))
        self.__config[key].sort()

    def _update_value(self, key, value, default_value):
        self.__config.setdefault(key, default_value)
        if value is not None:
            self.__config[key] = value

    @property
    def config(self):
        """

        :return: config as a dictionary
        """
        return self.__config

    @config.setter
    def config(self, config):
        self.__config = config

    @property
    def layers(self):
        """

        :return: list with positions for commits
            (between which commands shout be new layer)
        """
        return self.__config.get(CONFIG_LAYERS, [])

    @layers.setter
    def layers(self, layers):
        self.__config[CONFIG_LAYERS] = layers

    @property
    def volumes(self):
        """

        :return: Tuples with source:destination volume only for build.
        """
        return self.__config.get(CONFIG_VOLUMES, [])

    @volumes.setter
    def volumes(self, volumes):
        self.__config[CONFIG_VOLUMES] = volumes

    @property
    def labels(self):
        """

        :return: Label tuples, which should be added to image.
        """
        return self.__config.get(CONFIG_LABELS, [])

    @labels.setter
    def labels(self, labels):
        self.__config[CONFIG_LABELS] = labels

    @property
    def container_limits(self):
        return self.__config.get(CONFIG_CONTAINER_LIMITS, {})

    @container_limits.setter
    def container_limits(self, limits):
        self.__config[CONFIG_CONTAINER_LIMITS] = limits

    @property
    def version(self):
        """

        :return: Version of structure from json.
        """
        return self.__config.get(CONFIG_VERSION, DEFAULT_VERSION)

    @property
    def infinite_command(self):
        return self.__config.get(CONFIG_INFINITE_COMMAND, INFINITE_COMMAND)

    @infinite_command.setter
    def infinite_command(self, command):
        self.__config[CONFIG_INFINITE_COMMAND] = command

    @property
    def mkdir_command(self):
        return self.__config.get(CONFIG_MKDIR_COMMAND, MKDIR_COMMAND)

    @mkdir_command.setter
    def mkdir_command(self, command):
        self.__config[CONFIG_MKDIR_COMMAND] = command

    @property
    def tags(self):
        return self.__config.get(CONFIG_TAGS, [])

    @tags.setter
    def tags(self, tags):
        self.__config[CONFIG_TAGS] = tags

    @property
    def tags_and_repos(self):
        """
        :return: list with tupple (repo,tag)
        """
        result = []
        for t in self.tags:
            t_split = t.split(':')
            t_part_number = len(t_split)
            if t_part_number > 2:
                raise Exception("Wrong tag format.")
            elif t_part_number == 2:
                result.append((t_split[0], t_split[1]))
            elif t_part_number == 1:
                result.append((t, DEFAULT_TAG))
        return result

    @property
    def pull(self):
        return self.__config.get(CONFIG_PULL, False)

    @pull.setter
    def pull(self, pull):
        self.__config[CONFIG_TAGS] = pull

    def is_valid(self):
        """

        :return: True if the json structure is valid, else False.
        """
        try:
            self.validate()
            return True
        except jsonschema.exceptions.ValidationError:
            return False

    @property
    def context_file_limit(self):
        return self.__config.get(CONFIG_CONTEXT_FILE_LIMIT, -1)

    def validate(self):
        """

        :return: None if the structure of json is valid, else throws exceptions.
        """
        version = self.__config.get(CONFIG_VERSION, None)
        version_schema = schema.get(version, None)

        if version_schema is not None:
            jsonschema.validate(self.__config, schema)
            return None
        else:
            raise jsonschema.exceptions.ValidationError("Unknown config version.")
