from __future__ import absolute_import, print_function, unicode_literals

import apache_beam as beam

from dojo.transform import Transform
from dojo.transforms import Conform as VanillaConform, \
    Validate as VanillaValidate, \
    ConvertFrom as VanillaConvertFrom, \
    ConvertTo as VanillaConvertTo, \
    KeyBy as VanillaKeyBy, \
    DeKey as VanillaDeKey


class BeamTransform(Transform, beam.DoFn):

    def process(self, row):
        raise NotImplementedError()


class SetValue(BeamTransform):

    def __init__(self, key, value, *args, **kwargs):
        self.key = key
        self.value = value
        super(SetValue, self).__init__(*args, **kwargs)

    def process(self, row):
        row[self.key] = self.value
        return [row, ]


class Conform(VanillaConform, beam.DoFn):

    def process(self, row):
        # apache_beam.typehints.decorators.TypeCheckError: Returning a dict from a ParDo or FlatMap is discouraged
        return [super(Conform, self).process(row), ]


class Validate(VanillaValidate, beam.DoFn):

    def process(self, row):
        return [super(Validate, self).process(row), ]


class ConvertFrom(VanillaConvertFrom, beam.DoFn):

    def process(self, row):
        return [super(ConvertFrom, self).process(row), ]


class ConvertTo(VanillaConvertTo, beam.DoFn):

    def process(self, row):
        return [super(ConvertTo, self).process(row), ]


class KeyBy(VanillaKeyBy, beam.DoFn):

    def process(self, row):
        return [super(KeyBy, self).process(row), ]


class DeKey(VanillaDeKey, beam.DoFn):

    def process(self, row):
        return [super(DeKey, self).process(row), ]
