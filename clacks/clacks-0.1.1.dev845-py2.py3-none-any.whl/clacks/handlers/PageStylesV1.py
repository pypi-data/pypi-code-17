#!/usr/bin/env python3

"""PageStylesService handles /_v1/page-styles/ url namespace as REST calls."""

import cherrypy

from ..db import db
from ..gettext import gettext as _
from ..models import PageNode
from .URLHandler import URLHandler


class PageStyles(URLHandler):

    """PageStyles handles /_v1/page-styles/ url namespace as REST calls."""

    mount_url = '/_v1/page-styles'
    dispatcher = 'MethodDispatcher'
    exposed = True

    @cherrypy.tools.json_out()
    @cherrypy.tools.require(grant='SITE_STRUCTURE_VIEW')
    def GET(self, *, page=None):

        """List of styles supported by given page as JSON list of dictionaries."""

        if page:
            page = db.query(PageNode).get(int(page))
            allItems = page.styles()
            default = allItems.pop('', None)

            allItems = [{'id': key, 'label': _(val)} for key, val in allItems.items()]
            allItems.sort(key=lambda n: n['label'])
            if default is not None:
                allItems.insert(0, {'id': 'default', 'label': _(default)})
            return allItems
        else:
            raise cherrypy.HTTPError(501, 'Full page styles list not yet implemented')
