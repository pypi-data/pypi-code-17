from collections import OrderedDict


class SpecCache(object):
    def __init__(self, *specs):
        self.specs = OrderedDict()
        self.add_specs(*specs)

    def clear(self):
        self.specs = OrderedDict()

    def add_spec(self, spec):
        self.specs[spec.full_id] = spec

    def add_specs(self, *specs):
        for spec in specs:
            self.add_spec(spec)

    def get_spec(self, full_id):
        return self.specs[full_id]
