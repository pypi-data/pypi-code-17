# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

import abc
import six


@six.add_metaclass(abc.ABCMeta)
class BaseRequirement(object):
    """A single variable required by a scoring function

    Since several components of a scoring function may use
    the same parameters (for instance, both Coulomb and
    Lennard-Jones potential use a matrix of atomwise distance),
    requirements are the solution to only compute each
    parameter once.

    Requirements compute and preformat parameters using
    Python and numpy only (as opposed to actual components
    which compute results using linear algebra backends).
    """

    def __init__(self):
        pass
