import argparse
import logging

import yaml

try:
    import ujson as json
except:
    import json


class Option(object):
    def __init__(self, name, **kwargs):
        self.name = name
        self.type = kwargs.get('type', str)
        self.value = kwargs.get('default', self.type())
        self.help = kwargs.get('help', None)

    def set_value(self, v):
        if self.type is not dict and hasattr(self.type, '__call__'):
            self.value = self.type(v)
        elif isinstance(self.value, dict) and isinstance(v, dict):
            self.value.update(v)
        else:
            self.value = v

    def __str__(self):
        return '<Option name=%s, value=%s, type=%s, help=%s>' % (
            self.name,
            self.value,
            self.type,
            self.help
        )


class ConfMan(object):
    def __init__(self):
        self._values = {}

    def _bool(self, value):
        value = str(value).upper()
        return value in ['YES', 'TRUE', 'Y']

    def _list(self, value):
        return str(value).split(',')

    def parse_manage_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--config', type=str, help='config path', default=None)

        for key, value in self._values.items():
            arg_type = value.type
            if arg_type is bool:
                arg_type = self._bool
            if arg_type is list:
                arg_type = self._list

            parser.add_argument('--%s' % key, type=arg_type, default=None, help=value.help)

        kwargs = parser.parse_args()

        for k, v in vars(kwargs).items():
            if k == 'config':
                self.read_config(v)
                break

        for k, v in vars(kwargs).items():
            if k != 'config' and v is not None:
                self.set_value(k, v)

    def set_value(self, k, v):
        self._values[k].set_value(v)

    def defined(self, name):
        return name in self._values

    def define(self, name, **kwargs):
        if self.defined(name):
            raise AttributeError('%s already defined' % name)
        else:
            setattr(self, name, Option(name, **kwargs))

    def rawset(self, name, value):
        super(ConfMan, self).__setattr__(name, value)

    def read_config(self, path):
        if path is None:
            return

        with open(path) as f:
            success = False
            exceptions = []
            config = {}

            if not success:
                try:
                    config = yaml.load(f)
                    success = True
                except Exception as e:
                    exceptions.append(e)

            if not success:
                try:
                    f.seek(0)
                    config = json.load(f)
                    success = True
                except Exception as e:
                    exceptions.append(e)

            if not success:
                for e in exceptions:
                    logging.exception(e)
                raise Exception('Unable parse config')

            if not isinstance(config, dict):
                raise Exception('Config must be dict')

            for k, v in config.items():
                if self.defined(k):
                    self.set_value(k, v)
                else:
                    self.define(k, default=v, type=type(v))

    def __getattr__(self, name):
        if name == '_values':
            return self._values

        return self._values[name].value if name in self._values else None

    def __setattr__(self, name, value):
        if name in ['_values']:
            self.rawset(name, value)
        else:
            self._values[name] = value

    def __str__(self):
        config = {}
        for k, v in self._values.items():
            config[k] = v.value
        return json.dumps(config, indent=2)
