from __future__ import unicode_literals

from ..transform import SparkTransform


class SparkSQLTransform(SparkTransform):

    def process(self, inputs):
        for name, df in inputs.items():
            df.registerTempTable(name)
        return self.sql_context.sql(self.config['sql'])
