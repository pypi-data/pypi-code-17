from __future__ import unicode_literals


class Configurable(object):
    REQUIRED = []
    OPTIONAL = {}

    def configure(self, **options):
        for field in self.REQUIRED:
            if field not in options:
                raise ValueError('%s is required' % (field, ))
            setattr(self, field, options[field])
        for field, default in self.OPTIONAL.items():
            setattr(self, field, options.get(field, default))
