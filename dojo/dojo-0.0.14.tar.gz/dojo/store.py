from __future__ import unicode_literals

import os
import luigi

from datetime import datetime

from .configurable import Configurable


class SparkStore(luigi.Target, Configurable):
    REQUIRED = ['sql_context']

    TIMESTAMP_FORMAT = '%Y%m%d%H%M%S%f'

    spark_packages = []

    def __init__(self, config, secrets, dataset, format='json', flag='_SUCCESS'):
        self.config = config
        self.secrets = secrets
        self.dataset = dataset
        self.format = format
        self.flag = flag

    def __getstate__(self):
        state = self.__dict__.copy()
        if 'sql_context' in state:
            del state['sql_context']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def input_path(self):
        raise NotImplementedError()

    def exists(self):
        latest_path = self.input_path()
        if latest_path is None:
            return False
        latest_timestamp = self._timestamp_from_path(latest_path)
        return latest_timestamp >= self._beginning_of_period()

    def read(self):
        return self._formatted_io(self.sql_context.read, self.input_uri())

    def write(self, df):
        df = df.repartition(1)
        # TODO: remove this hard coded partition count
        return self._formatted_io(df.write, self.output_uri())

    def read_file(self, path):
        raise NotImplementedError()

    def write_file(self, path, file):
        raise NotImplementedError()

    def _formatted_io(self, io, path):
        if self.format == 'parquet':
            return io.parquet(path)
        elif self.format == 'json':
            return io.json(path)
        raise ValueError('invalid format %s' % (self.format, ))

    def input_uri(self):
        return '%s://%s' % (self.config['protocol'], self.input_path())

    def output_uri(self):
        return '%s://%s' % (self.config['protocol'], self.output_path())

    def output_path(self):
        return os.path.join(self._dataset_path(), self.timestamp.strftime(self.TIMESTAMP_FORMAT))

    def files_output_path(self):
        return os.path.join(self._dataset_path('files'), self.timestamp.strftime(self.TIMESTAMP_FORMAT))

    def _dataset_path(self, prefix='data'):
        path = os.path.join(prefix, self.dataset)
        if 'root_path' in self.config:
            path = os.path.join(self.config['root_path'], path)
        return path

    def _timestamp_from_path(self, path):
        period = path.split('/')[-1]
        return self._timestamp_from_period(period)

    def _timestamp_from_period(self, period):
        return datetime.strptime(period, self.TIMESTAMP_FORMAT)

    def _beginning_of_period(self):
        truncate_kwargs = {
            'day': {'hour': 0, 'minute': 0, 'second': 0, 'microsecond': 0},
            'hour': {'minute': 0, 'second': 0, 'microsecond': 0},
            'minute': {'second': 0, 'microsecond': 0},
            'second': {'microsecond': 0},
            'microsecond': {}
        }
        if isinstance(self.frequency, tuple):
            self.frequency = self.frequency[0]
        if self.frequency not in truncate_kwargs.keys():
            raise ValueError('frequency %s not implemented' % (self.frequency, ))
        kwargs = truncate_kwargs[self.frequency]
        return self.timestamp.replace(**kwargs)
