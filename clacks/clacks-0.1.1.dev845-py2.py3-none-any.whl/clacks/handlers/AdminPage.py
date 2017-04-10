#!/usr/bin/env python3

"""AdminPage handler."""

import cherrypy

from ..core import cfg, env
from ..core.BasePage import BasePage
from ..core.templates import templates
from .URLHandler import URLHandler


class AdminPage(BasePage, URLHandler):

    """AdminPage handler."""

    mount_url = '/_admin'

    def __init__(self):
        super().__init__()
        self.addDependencies(cfg.get('page', 'dependencies', '_admin', default={}))

    def deps(self):
        """ needs to be replaced with getDependencies() when all remainings
        of old panel will be dropped

        \todo removal of hardcoded /_css/admin.css
        """

        return {'dojo': [{'src': 'gtcms/admin'}],
                'css': [{'src': '/_css/admin.css'}]+self.getDependencies().get('css', []),
                'dojoPackages': self.getDependencies().get('dojoPackages', []),
                'javascript': self.getDependencies().get('javascript', [])}

    @cherrypy.expose
    @cherrypy.tools.require(user_state=True)
    def index(self):
        """Return main (and only) admin panel page"""
        if not getattr(cherrypy.request, 'user', None) and \
           cfg.get('env', 'admin_login_url', default=None):
            raise cherrypy.HTTPRedirect(cfg.get('env', 'admin_login_url'))
        expVars = {'ctx': self, 'cfg': cfg, 'Env': env}
        return templates['page_admin'](**expVars)
