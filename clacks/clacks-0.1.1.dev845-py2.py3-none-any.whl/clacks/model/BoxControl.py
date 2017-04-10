#!/usr/bin/env python3

"""BoxControl class."""

import cherrypy

from ..core.templates import templates
from ..db import db
from ..gettext import gettext as _
from ..tools import structural
from .Box import Box
from .Control import Control


class BoxControl(Control):

    """BoxControl class."""

    __mapper_args__ = {'polymorphic_identity': 'Box'}
    _settings = {'default-placements': ()}

    @classmethod
    def controlName(cls):
        return _('Text box')

    @property
    def name(self):
        """ name used in administration panel """
        if 'boxid' in self.properties:
            label = db.query(Box).get(int(self.properties['boxid'])).label
            if label:
                return _('Text box (%s)') % (label,)
        return self.controlName()

    @property
    def url(self):
        """Return assinged url or empty string if not given."""
        return self.properties.get('url', '')

    @property
    def style(self):
        """template style to use"""
        return self.properties.get('style', '')

    @property
    def box(self):
        """ related box containing content """
        return db.query(Box).get(self.properties.get('boxid', 0))

    @property
    def grant(self):
        """ if set, this grant is required to see contents """
        return self.properties.get('grants', None)

    @structural
    def fetch(self, placement):    # pylint: disable=unused-argument

        """ fetch control's content"""

        if not self.style or not self.box:
            return ''

        try:
            user = cherrypy.request.user
        except AttributeError:
            pass
        else:
            if self.grant and not (user and user.granted(self.grant)):
                return ''

        if not self.box:
            return ''

        return templates.first('control_box_'+self.style,
                               'control_box_default')(this=self)
