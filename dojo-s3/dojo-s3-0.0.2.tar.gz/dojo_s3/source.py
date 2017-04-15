from __future__ import unicode_literals

import os
import boto3
import botocore

from dojo.source import SparkSource


class SparkS3Source(SparkSource):

    spark_packages = ['org.apache.hadoop:hadoop-aws:2.7.0', ]

    def read(self, inputs):
        raise NotImplementedError()
