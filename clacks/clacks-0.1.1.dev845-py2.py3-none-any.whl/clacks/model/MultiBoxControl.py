#!/usr/bin/env python3
# pylint: disable=attribute-defined-outside-init
"""MultiBoxControl class."""

from sqlalchemy.orm import reconstructor

from ..db import db
from ..core.templates import templates
from ..gettext import gettext as _
from ..tools import structural
from .Box import Box
from .Control import Control


class MultiBoxControl(Control):

    """MultiBoxControl class."""

    __mapper_args__ = {'polymorphic_identity': 'MultiBox'}
    _settings = {'default-placements': ('abovebody', 'belowbody', 'footer')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._reconstructor()

    @reconstructor
    def _reconstructor(self):
        """Create additional fields when object is restored from db """
        self._boxes = None
        self._random = None

    @classmethod
    def controlName(cls):
        return _('Text boxes list')

    @property
    def style(self):
        """template style to use"""
        return self.properties.get('style', '')

    @property
    def boxes(self):
        """ return connected boxes list """
        if self._boxes is None:
            ids = self.properties.get('boxids', '')
            if ids:
                idlist = [int(id) for id in ids.split(',')]
                # this way all boxes are fetched from db in one go:
                db.query(Box).filter(Box.id.in_(idlist)).all()
                # little trick, as now we need them in idlist order
                result = (db.query(Box).get(id) for id in idlist)
                self._boxes = [box for box in result if box]
            else:
                self._boxes = []
        return self._boxes

    @property
    def random(self):
        """Return random box, but the same for the lifetime of object.
           (Needs optimization not to load all boxes unnecessarily).
        """
        from random import choice
        if self._random is None:
            self._random = choice(self.boxes)
        return self._random

    @structural
    def fetch(self, placement):    # pylint: disable=unused-argument
        """ fetch control's content"""

        return templates.first('control_multiBox_'+self.style,
                               'control_multiBox_default')(this=self)
