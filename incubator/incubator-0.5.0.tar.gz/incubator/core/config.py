"""
Class for managing configuration.
"""
import json
import logging
import os

import jsonschema
import six
from jsonschema import Draft3Validator

from .constants import (APP_NAME, CONFIG_BUILDARGS, CONFIG_CONTAINER_LIMITS,
                        CONFIG_CONTEXT_FILE_LIMIT, CONFIG_FORCE_RM,
                        CONFIG_INFINITE_COMMAND, CONFIG_LABELS, CONFIG_LAYERS,
                        CONFIG_MKDIR_COMMAND, CONFIG_NAME, CONFIG_PULL,
                        CONFIG_RM, CONFIG_TAGS, CONFIG_VERSION, CONFIG_VOLUMES,
                        DEFAULT_CONFIG_FILES, DEFAULT_CONTEXT_FILE_LIMIT,
                        DEFAULT_FORCE_RM, DEFAULT_INFINITE_COMMAND,
                        DEFAULT_MKDIR_COMMAND, DEFAULT_PULL, DEFAULT_RM,
                        DEFAULT_TAG, DEFAULT_VERSION)

logger = logging.getLogger(APP_NAME)

schema_v1 = {
    "type": "object",
    "properties": {
        CONFIG_VERSION: {"type": "number"},
        CONFIG_NAME: {"type": "string"},
        CONFIG_BUILDARGS: {
            "type": "object",
            "patternProperties": {
                "": {
                    "type": "string"
                }
            }
        },
        CONFIG_CONTAINER_LIMITS: {
            "type": "object",
            "properties": {},
            "patternProperties": {
                "": {
                    "type": "string"
                }
            }
        },
        CONFIG_CONTEXT_FILE_LIMIT: {'type': 'integer'},
        CONFIG_FORCE_RM: {'type': 'boolean'},
        CONFIG_LAYERS: {
            "type": "array",
            "items": {
                "type": "integer",
                "minimum": 0
            },
        },
        CONFIG_VOLUMES: {
            "type": "array",
            "properties": {},
            "patternProperties": {
                "": {
                    "type": "string"
                }
            }
        },
        CONFIG_LABELS: {
            "type": "object",
            "properties": {},
            "patternProperties": {
                "": {
                    "type": "string"
                }
            }
        },
        CONFIG_INFINITE_COMMAND: {"type": "string"},
        CONFIG_MKDIR_COMMAND: {"type": "string"},
        CONFIG_PULL: {"type": "boolean"},
        CONFIG_RM: {"type": "boolean"},
        CONFIG_TAGS: {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    },
    "additionalProperties": False
}

schema = {1.0: schema_v1}


class ImageConfig(object):
    """
    Representation of config file.
    Structure of file is described and validated by jsonschema.
    """

    def __init__(self, config_dict=None):

        config_dict = config_dict or {}

        if not self.validate_json_schema(config=config_dict):
            raise Exception("Config not valid.")

        name_str = config_dict.get(CONFIG_NAME)
        self._name = [name_str] if name_str else []
        self._buildargs = config_dict.get(CONFIG_BUILDARGS)
        self._container_limits = config_dict.get(CONFIG_CONTAINER_LIMITS)
        self._context_file_limit = config_dict.get(CONFIG_CONTEXT_FILE_LIMIT)
        self._forcerm = config_dict.get(CONFIG_FORCE_RM)
        self._infinite_command = config_dict.get(CONFIG_INFINITE_COMMAND)
        self._labels = config_dict.get(CONFIG_LABELS)

        layers = config_dict.get(CONFIG_LAYERS)
        if layers is not None:
            self._layers = sorted(set(layers))
        else:
            self._layers = None

        self._mkdir_command = config_dict.get(CONFIG_MKDIR_COMMAND)
        self._pull = config_dict.get(CONFIG_PULL)
        self._rm = config_dict.get(CONFIG_RM)
        self._tags = config_dict.get(CONFIG_TAGS)
        self._volumes = config_dict.get(CONFIG_VOLUMES)

    @property
    def config(self):
        d = {}
        if self._buildargs is not None:
            d[CONFIG_BUILDARGS] = dict(self._buildargs)
        if self._container_limits is not None:
            d[CONFIG_CONTAINER_LIMITS] = dict(self._container_limits)
        if self._context_file_limit:
            d[CONFIG_CONTEXT_FILE_LIMIT] = self._context_file_limit
        if self._forcerm is not None:
            d[CONFIG_FORCE_RM] = self._forcerm
        if self._infinite_command:
            d[CONFIG_INFINITE_COMMAND] = self._infinite_command
        if self._labels is not None:
            d[CONFIG_LABELS] = dict(self._labels)
        if self._layers is not None:
            d[CONFIG_LAYERS] = list(self._layers)
        if self._mkdir_command:
            d[CONFIG_MKDIR_COMMAND] = self._mkdir_command
        if self._pull is not None:
            d[CONFIG_PULL] = self._pull
        if self._rm is not None:
            d[CONFIG_RM] = self._rm
        if self._tags is not None:
            d[CONFIG_TAGS] = list(self._tags)
        if self._volumes is not None:
            d[CONFIG_VOLUMES] = list(self._volumes)

        return d

    @property
    def buildargs(self):
        return self._buildargs or {}

    @buildargs.setter
    def buildargs(self, value):
        self.build_args = value

    @property
    def container_limits(self):
        return self._container_limits or {}

    @container_limits.setter
    def container_limits(self, limits):
        self._container_limits = limits

    @property
    def context_file_limit(self):
        return self._context_file_limit or DEFAULT_CONTEXT_FILE_LIMIT

    @context_file_limit.setter
    def context_file_limit(self, value):
        self._context_file_limit = value

    @property
    def forcerm(self):
        return self._forcerm if self._forcerm is not None else DEFAULT_FORCE_RM

    @forcerm.setter
    def forcerm(self, value):
        self._forcerm = value

    @property
    def infinite_command(self):
        return self._infinite_command or DEFAULT_INFINITE_COMMAND

    @infinite_command.setter
    def infinite_command(self, value):
        self._infinite_command = value

    @property
    def labels(self):
        return self._labels or {}

    @labels.setter
    def labels(self, value):
        self._labels = value

    @property
    def layers(self):
        return self._layers or []

    @layers.setter
    def layers(self, value):
        self._layers = value

    @property
    def mkdir_command(self):
        return self._mkdir_command or DEFAULT_MKDIR_COMMAND

    @mkdir_command.setter
    def mkdir_command(self, value):
        self._mkdir_command = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def pull(self):
        return self._pull if self._pull is not None else DEFAULT_PULL

    @pull.setter
    def pull(self, value):
        self._pull = value

    @property
    def rm(self):
        return self._rm if self._rm is not None else DEFAULT_RM

    @rm.setter
    def rm(self, value):
        self._rm = value

    @property
    def tags(self):
        return self._tags or []

    @tags.setter
    def tags(self, value):
        self.tags = value

    @property
    def volumes(self):
        """

        :return: Tuples with source:destination volume only for build.
        """
        return self._volumes or []

    @volumes.setter
    def volumes(self, value):
        self._volumes = value

    def update(self, buildargs=None,
               container_limits=None,
               context_file_limit=None,
               forcerm=None,
               infinite_command=None,
               labels=None,
               layers=None,
               mkdir_command=None,
               pull=None,
               rm=None,
               tags=None,
               volumes=None):
        self._buildargs = self._update_dict(self._buildargs, buildargs)
        self._container_limits = self._update_dict(self._container_limits, container_limits)
        self._context_file_limit = self._update_value(self._context_file_limit, context_file_limit)
        self._forcerm = self._update_value(self._forcerm, forcerm)
        self._infinite_command = self._update_value(self._infinite_command, infinite_command)
        self._labels = self._update_dict(self._labels, labels)
        self._layers = self._update_value(self._layers, layers)
        self._mkdir_command = self._update_value(self._mkdir_command, mkdir_command)
        self._pull = self._update_value(self._pull, pull)
        self._rm = self._update_value(self._rm, rm)
        self._tags = self._update_list(self._tags, tags)
        self._volumes = self._update_list(self._volumes, volumes)

    @staticmethod
    def _update_dict(origin, other):
        if (origin is None) and (other is None):
            return None

        result_dict = {}
        result_dict.update(origin or {})
        result_dict.update(other or {})
        return result_dict

    @staticmethod
    def _update_value(origin, other):
        return other if other is not None else origin

    @staticmethod
    def _update_list(origin, other):
        if (origin is None) and (other is None):
            return None
        result_list = origin or []

        if isinstance(other, six.string_types):
            result_list.append(other)
        elif other is not None:
            result_list += other

        return result_list

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

    @staticmethod
    def validate_json_schema(config):
        """
        :return: True, if the config dictionary is valid. Else false.
        """

        try:
            name = config.get(CONFIG_NAME, "")
        except:
            name = ""

        try:
            version = config.get(CONFIG_VERSION, DEFAULT_VERSION)
            version_schema = schema.get(version)
            if not version_schema:
                raise Exception("Config version is not valid.")
            Draft3Validator(version_schema).validate(config)
            return True
        except jsonschema.ValidationError as ex:
            logger.warning("Config '{}' is not valid:\n{}".format(name, ex.message))
            return False
        except:
            logger.warning("Version for config '{}' is not valid.".format(name))
            return False

    @staticmethod
    def load_config_from_default_files():
        configs = []
        for f in DEFAULT_CONFIG_FILES:
            try:
                abs_path = os.path.normpath(os.path.abspath(f))
                if os.path.exists(abs_path):
                    logger.debug("Loading default config `{}`".format(f))
                    with open(f, mode='r') as config_file:
                        config_dict = json.load(config_file)
                        config_dict.setdefault(CONFIG_NAME, f)
                        configs.append(config_dict)
            except Exception as ex:
                message = "Cannot load default config file '{}':\n{}".format(f, ex.msg)
                logger.warning(message)

        return configs

    @staticmethod
    def merge_configs(config):
        config_object = ImageConfig()
        if config:
            if not isinstance(config, list):
                config = [config]
            for c in config:
                config_object += ImageConfig(config_dict=c)
        return config_object

    def __add__(self, other):
        first_dictionary = self.config
        second_dictionary = other.config

        new = ImageConfig(config_dict=first_dictionary)
        new.update(**second_dictionary)
        new.name = self.name + other.name
        return new
