from __future__ import unicode_literals

import os
import simplejson as json
import yaml
import luigi

from dojo.flow import Flow


class Config(object):

    def __init__(self):
        self._dir = '/app'
        self._read_config()
        self._read_secrets()
        self._read_schemas()

    def _read_config(self):
        config = {}
        if os.path.isfile(self._path('dojo.json')):
            config.update(self._read_json_config())
        if os.path.isfile(self._path('dojo.yml')):
            config.update(self._read_yaml_config())
        self.config = config
        self.name = config['name']

    def _read_json_config(self):
        with open(self._path('dojo.json'), 'r') as f:
            return json.loads(f.read())

    def _read_yaml_config(self):
        with open(self._path('dojo.yml'), 'r') as f:
            return yaml.load(f)

    def _read_schemas(self):
        for dataset_name, dataset in self.config['datasets'].items():
            schema_path = os.path.join(self._path('schemas'), '%s.json' % (dataset_name, ))
            if os.path.isfile(schema_path):
                with open(schema_path, 'r') as f:
                    self.config['datasets'][dataset_name]['schema'] = json.loads(f.read())

    def _read_secrets(self):
        with open(self._path('secrets.json'), 'r') as f:
            self.secrets = json.loads(f.read())

    def _path(self, path):
        return os.path.join(self._dir, path)


class Runner(object):

    def __init__(self):
        config = Config()
        self.task = Flow(name=config.name)
        self.task.configure(
            config=config.config,
            secrets=config.secrets
        )

    def run(self):
        luigi.build([self.task, ], local_scheduler=True)


if __name__ == '__main__':
    runner = Runner()
    runner.run()
