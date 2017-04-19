# -*- coding: utf-8 -*-
"""
jaeum_modifier.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements custom exceptions.
"""


class NoIndexFoundError(LookupError):
    """Specified index runs out of bounds on the given unicode string.
    """
    # TODO: Maybe use IndexError?
    pass


class NoComplexityFoundError(LookupError):
    """There is no eumjul with desired complexity.
    """
    # TODO: Is there any exception that is closer?
    # TODO: Do we even need to use a specific Exception?
    pass


class InvalidJaeumError(TypeError):
    """Expected Jaeum, but failed Jauem test.
    """
    pass


class InvalidHangulError(TypeError):
    """Expected Hangul, but failed Hangul test.
    """
    pass
