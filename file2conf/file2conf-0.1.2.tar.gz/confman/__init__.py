from .confman import ConfMan

options = ConfMan()


def define(name, **kwargs):
    options.define(name, **kwargs)
