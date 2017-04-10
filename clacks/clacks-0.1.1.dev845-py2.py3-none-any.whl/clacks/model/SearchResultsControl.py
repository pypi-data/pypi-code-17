#!/usr/bin/env python3

"""SearchResultsControl class."""

from ..gettext import gettext as _

from .Control import Control


class SearchResultsControl(Control):

    """SearchResultsControl class."""

    __mapper_args__ = {'polymorphic_identity': 'SearchResults'}

    _settings = {'default-placements': ('belowbody',),
                 'one-per-language': True,
                 'node-types': ('article')}

    editMode = None

    @classmethod
    def controlName(cls):
        return _('Search contents results')
