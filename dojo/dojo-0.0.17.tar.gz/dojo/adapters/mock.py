from __future__ import unicode_literals

from ..source import SparkSource
from ..transform import SparkTransform
from ..sink import SparkSink
from .local_file_system import SparkLocalFileSystemStore


class MockStore(SparkLocalFileSystemStore):
    pass


class MockSource(SparkSource):

    def read(self, inputs):
        return self.to_df(self.config['data'])


class MockTransform(SparkTransform):

    def process(self, inputs):
        inputs = {name: self.to_df(rows) for name, rows in self.config['inputs'].items()}
        rdd = list(inputs.values())[0].rdd.map(lambda row: row.asDict())
        return rdd.map(self.config['function'])\
                  .toDF()


class MockSink(SparkSink):

    def exists(self):
        return not not self.config['data']

    def write(self, df):
        df = self.to_df(self.config['data'])
        self.mock_write_data = [row.asDict() for row in df.collect()]
