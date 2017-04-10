#!/usr/bin/env python3

"""/_v1/site-node-placements service handler."""

import cherrypy

from ..db import db
from ..gettext import gettext as _
from ..models import SiteNode
from .URLHandler import URLHandler


class PagePlacements(URLHandler):
    """/_v1/site-node-placements service handler."""

    mount_url = '/_v1/site-node-placements'

    @cherrypy.expose
    @cherrypy.tools.require(grant='SITE_STRUCTURE_VIEW')
    @cherrypy.tools.json_out()
    def default(self, *, page=None):
        """Return list of possible page placement settings."""
        if page:
            page = db.query(SiteNode).get(int(page))
            return sorted(({'id': key, 'label': val}
                           for key, val in page.placements().items()),
                          key=lambda n: n['label'] if n['id'] != '' else '')
        else:
            raise cherrypy.HTTPError(400, _('Full list of possible page placements is not supported'))
