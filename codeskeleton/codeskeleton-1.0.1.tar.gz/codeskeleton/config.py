import os

import yaml

from codeskeleton import exceptions
from codeskeleton.exceptions import ConfigFileError


class Config(object):
    """
    Config file parser
    """

    @classmethod
    def load_or_create(cls, configpath=os.path.expanduser('~/.codeskeleton.config.yaml')):
        config = cls(path=configpath)
        if os.path.exists(configpath):
            config.load_from_disk()
        else:
            # Create config file if it does not exist
            config.save_to_disk()
        return config

    def __init__(self, path):
        self.path = path
        self.spec_directories = set()

    def register_spec_directory(self, spec_directory):
        self.spec_directories.add(os.path.abspath(spec_directory))

    def unregister_spec_directory(self, spec_directory):
        self.spec_directories.remove(os.path.abspath(spec_directory))

    def has_spec_directory(self, spec_directory):
        return os.path.abspath(spec_directory) in self.spec_directories

    def update_from_dict(self, configdict):
        for spec_directory in configdict.get('spec_directories', []):
            self.register_spec_directory(spec_directory)

    def serialize(self):
        return {
            'spec_directories': list(sorted(self.spec_directories))
        }

    def load_from_disk(self):
        try:
            raw_yaml = open(self.path, 'r').read()
        except IOError:
            raise ConfigFileError(
                'Could not open the config file: {path!r}'.format(
                    path=self.path
                ))
        else:
            try:
                configdict = yaml.safe_load(raw_yaml)
            except yaml.YAMLError as e:
                raise exceptions.ConfigFileError('Failed to parse config file YAML: {}'.format(e))
            else:
                self.update_from_dict(configdict)

    def save_to_disk(self):
        with open(self.path, 'w') as f:
            f.write(yaml.safe_dump(self.serialize(), indent=4, default_flow_style=False))
