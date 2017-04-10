#!/usr/bin/env python3

"""RestrictedAccessControl class"""

import cherrypy

from ..db import db
from ..gettext import gettext as _
from .Control import Control
from .ControlProperty import ControlProperty
from .PageNode import PageNode


class RestrictedAccessControl(Control):
    """RestrictedAccessControl class"""

    __mapper_args__ = {'polymorphic_identity': 'RestrictedAccess'}
    _settings = {'default-placements': ('dummy',),
                 'one-per-page': True,
                 'node-types': ('article')}
    editMode = None

    @classmethod
    def controlName(cls):
        return _('Restrict anonymous access')

    @property
    def placements(self):
        return []

    def startup(self, node):

        if self.properties.get('landing_page', False):
            if cherrypy.request.user:
                if cherrypy.request.params.get('ref', False):
                    raise cherrypy.HTTPRedirect(
                        db.query(PageNode).get(cherrypy.request.params.get('ref', False)).url)
                else:
                    raise cherrypy.HTTPRedirect('/')

        # if this control is assigned to meta page and current page has its
        # own instance, do nothing
        elif ((self.page is not node) and
              any(c._class == 'RestrictedAccess' for c in node.controls)):
            return
        elif not cherrypy.request.user and not getattr(cherrypy.request, 'printMode', False):
            target = db.query(RestrictedAccessControl)\
                       .join(ControlProperty, PageNode)\
                       .filter(ControlProperty.name == 'landing_page',
                               ControlProperty.value == 'true',
                               PageNode.lang == node.lang)\
                       .first()
            if target:
                raise cherrypy.HTTPRedirect(target.page.url+'?ref='+str(node.id))
