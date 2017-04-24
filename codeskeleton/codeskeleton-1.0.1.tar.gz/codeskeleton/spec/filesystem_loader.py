import os

import yaml

from codeskeleton import yaml_loader


class FileSystemLoader(object):
    def __init__(self, config, spec_class):
        self.config = config
        self.spec_class = spec_class
        self.spec_type = spec_class.__name__.lower()

    def _load_spec(self, spec_file):
        spec = self.spec_class(base_directory=os.path.dirname(spec_file))
        rawdata = open(spec_file, 'r').read()
        data = yaml.load(rawdata, Loader=yaml_loader.OrderedDictSafeLoader)
        spec.deserialize(data=data)
        return spec

    def _find_specs_in_spec_directory(self, spec_directory):
        specs = []
        for directory in os.listdir(spec_directory):
            spec_file = os.path.join(spec_directory, directory, 'codeskeleton.{}.yaml'.format(self.spec_type))
            if os.path.exists(spec_file):
                specs.append(self._load_spec(spec_file))
        return specs

    def find(self):
        specs = []
        for directory in self.config.spec_directories:
            spec_directory = os.path.join(directory, '{}s'.format(self.spec_type))
            if os.path.isdir(spec_directory):
                specs.extend(self._find_specs_in_spec_directory(spec_directory))
        return specs
