from __future__ import unicode_literals

from dojo.source import SparkSource


class SparkJDBCSource(SparkSource):

    spark_packages = ['mysql:mysql-connector-java:5.1.39', ]

    def read(self, inputs):
        if len(inputs) > 0:
            raise NotImplementedError()
        return self.sql_context.read\
                   .format('jdbc')\
                   .options(**self._credentials())\
                   .option('dbtable', self.config['table'])\
                   .load()

    def _credentials(self):
        return {
            'url': 'jdbc:%s://%s/%s' % (self.config['scheme'], self.secrets['host'], self.secrets['database']),
            'driver': 'com.%s.jdbc.Driver' % (self.config['scheme'], ),
            'user': self.secrets['user'],
            'password': self.secrets['password']
        }
