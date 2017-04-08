from siftpy._exceptions import ValidationException

class SiftValidator(object):
    def __init__(self, config):
        self.config = config

    def validate(self, data):
        if data.__class__ is not dict:
            raise ValidationException("Sifts must be initialized with a valid 'dict' object.")

        if self.config.SiftPropertyKey.Sifts in data and self.config.SiftPropertyKey.ContextSource in data:
            raise ValidationException("Either '{}' or '{}' may defined in a sift, but not both.".format(self.config.SiftPropertyKey.Sifts, self.config.SiftPropertyKey.ContextSource))

        if self.config.SiftPropertyKey.AggregationType in data and data[self.config.SiftPropertyKey.AggregationType] not in (
            [getattr(self.config.SiftAggregationType, key) for key in ("Combine", "ChooseSource", "ChooseElement", "Operation")]):
            raise ValidationException("'{}' is not a valid value for field '{}'.".format(data[self.config.SiftPropertyKey.AggregationType], self.config.SiftPropertyKey.AggregationType))
