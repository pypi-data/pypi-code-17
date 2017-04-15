from __future__ import unicode_literals

import os
import io
import boto3
import botocore

from dojo.store import SparkStore


class SparkS3Store(SparkStore):

    spark_packages = ['org.apache.hadoop:hadoop-aws:2.7.0', ]

    def __init__(self, *args, **kwargs):
        super(SparkS3Store, self).__init__(*args, **kwargs)
        self.config['protocol'] = 's3a'

    def configure(self, **kwargs):
        super(SparkS3Store, self).configure(**kwargs)
        self.sql_context._sc._jsc.hadoopConfiguration().set('fs.s3a.access.key', self.secrets['aws_access_key_id'])
        self.sql_context._sc._jsc.hadoopConfiguration().set('fs.s3a.secret.key', self.secrets['aws_secret_access_key'])

    def read_file(self, full_path):
        return self._s3().get_object(
            Bucket=self.config['bucket'],
            Key=full_path
        )['Body']

    def write_file(self, path, file):
        output_path = os.path.join(self.files_output_path(), path)
        self._s3().put_object(
            Bucket=self.config['bucket'],
            Key=output_path,
            Body=file.read())
        return output_path

    def input_path(self):
        prefix = self._dataset_path() + '/'
        result = self._s3().list_objects(Bucket=self.config['bucket'], Prefix=prefix, Delimiter='/')
        for obj in reversed(result.get('CommonPrefixes', [])):
            flag_path = os.path.join(obj.get('Prefix'), self.flag)
            if self._s3_key_exists(flag_path):
                return obj.get('Prefix')[:-1]

    def input_uri(self):
        return '%s://%s/%s' % (self.config['protocol'], self.config['bucket'], self.input_path())

    def output_uri(self):
        return '%s://%s/%s' % (self.config['protocol'], self.config['bucket'], self.output_path())

    def _s3(self):
        return boto3.client('s3', aws_access_key_id=self.secrets['aws_access_key_id'],
                            aws_secret_access_key=self.secrets['aws_secret_access_key'])

    def _s3_key_exists(self, path):
        try:
            self._s3().head_object(Bucket=self.config['bucket'], Key=path)
            return True
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                raise
