#!/usr/bin/env python3

"""/_v1/controls-appendable/ url service handler."""

import cherrypy

from ..core import cfg
from ..db import db
from ..gettext import gettext as _
from ..models import SiteNode
from .URLHandler import URLHandler


class ControlsAppendable(URLHandler):

    """/_v1/controls-appendable/ url service handler."""

    mount_url = '/_v1/controls-appendable'

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.require(grant='SITE_STRUCTURE_VIEW')
    def default(self, *, nodeid):
        """give all possible Controls and their placements allowed to be added to a given page.
        """
        node = db.query(SiteNode).get(nodeid)
        controls = node.getAppendableControls()
        names = cfg.get('controls', 'placement-names')

        return sorted(
            ({'id': ':'.join((c['control'].getIdentity(), location)),
              'fullname': (c['control'].controlName() +
                           ((' (%s)' % _(names[location])) if len(c['placements']) > 1 else '')),
              'location': location,
              'type': c['control'].getIdentity()}
             for c in controls for location in c['placements']),
            key=lambda k: k['fullname'])
