from __future__ import unicode_literals

from .task import SparkTask


class SparkSource(SparkTask):

    def read(self, inputs):
        raise NotImplementedError()

    def process(self, inputs):
        return self.read(inputs)
