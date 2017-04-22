from __future__ import unicode_literals

from .task import SparkTask


class SparkTransform(SparkTask):

    def process(self, inputs):
        raise NotImplementedError()
