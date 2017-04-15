from __future__ import unicode_literals

from ..source import SparkSource
from ..decoders.yaml import YAMLDecoder
from ..decoders.json import JSONDecoder


class ObjectSource(SparkSource):

    DECODERS = {
        'application/yaml': YAMLDecoder,
        'application/json': JSONDecoder,
    }

    def read(self, inputs):
        raise NotImplementedError()

    def decode(self, body, mime_type):
        decoder = self.DECODERS[mime_type]()
        return decoder.process(body)
