#!/usr/bin/env python3

""" SiteNodeTemplates handler """

import sys
import cherrypy

from ..core import cfg
from ..db import db
from ..models import SiteNode

from .URLHandler import URLHandler


class SiteNodeTemplates(URLHandler):

    """ SiteNodeTemplates handler """

    dispatcher = 'MethodDispatcher'
    mount_url = '/_v1/site-node-templates'
    exposed = True

    @cherrypy.tools.json_out()
    @cherrypy.tools.require(grant='SITE_STRUCTURE_VIEW')
    def GET(self, parent_page):
        """ returns list of supported factory page creators for given parent page
        """

        page = db.query(SiteNode).get(int(parent_page))
        methods = {}
        for fdata in cfg.get('page', 'factory').values():
            __import__(fdata['module'])
            methods.update(getattr(sys.modules[fdata['module']],
                                   fdata['factory']).getTemplates(page))
        return [{'id': k, 'name': v} for k, v in sorted(methods.items())]
