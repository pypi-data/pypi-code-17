from __future__ import unicode_literals

from .task import SparkTask


class SparkSink(SparkTask):

    def exists(self, inputs):
        raise NotImplementedError()

    def process(self, df):
        self.write(df)

    def write(self, df):
        df = df.repartition(4)
        # TODO: remove this partition count
        return self._formatted_io(df.write, self._target_uri(self.path))

    def _formatted_io(self, io, path):
        if self.format == 'parquet':
            return io.parquet(path)
        elif self.format == 'json':
            return io.json(path)
        raise ValueError('invalid format %s' % (self.format, ))

    def _target_uri(self, path):
        return '%s%s/%s/' % (self.scheme, self.config['root_path'], self._target_path(path), )

    def _target_path(self, path):
        return os.path.join(path, self.dataset, self.timestamp.strftime('%Y%m%d%H%M%S%f'))
