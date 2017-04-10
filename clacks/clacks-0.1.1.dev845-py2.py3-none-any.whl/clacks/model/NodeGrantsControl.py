#!/usr/bin/env python3

"""NodeGrants class"""

from ..gettext import gettext as _

from .Control import Control


class NodeGrantsControl(Control):

    """NodeGrantsControl class"""

    __mapper_args__ = {'polymorphic_identity': 'NodeGrants'}
    _settings = {'default-placements': ('dummy',),
                 'one-per-page': True}

    editMode = 'ControlPane'

    @classmethod
    def controlName(cls):
        return _('Grants')
