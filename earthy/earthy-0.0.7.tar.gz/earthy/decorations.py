# -*- coding: utf-8 -*-

def override(method):
    """ Decorator to add the `is_overriden` attribute to subclasses. """
    method.is_overridden = True
    return method
