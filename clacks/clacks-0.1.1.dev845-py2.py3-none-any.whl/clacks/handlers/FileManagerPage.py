#!/usr/bin/env python3

"""FileManagerPage handler."""

import cherrypy

from ..core import cfg, env
from ..core.BasePage import BasePage
from ..core.templates import templates
from .URLHandler import URLHandler


class FileManagerPage(BasePage, URLHandler):
    """AdminPage handler."""

    mount_url = '/_filemanager'

    def __init__(self):
        super().__init__()
        self.addDependencies(cfg.get('page', 'dependencies', '_filemanager', default={}))

    def deps(self):
        """ needs to be replaced with getDependencies() when all remainings
        of old panel will be dropped

        \todo removal of hardcoded /_css/admin.css
        """

        return {'dojo': self.getDependencies().get('dojo', []),
                'css': self.getDependencies().get('css', []),
                'dojoPackages': self.getDependencies().get('dojoPackages', []),
                'javascript': self.getDependencies().get('javascript', [])}

    @cherrypy.expose
    @cherrypy.tools.require(user_state=True)
    def index(self):
        """Return main (and only) admin panel page"""

        expVars = {'ctx': self, 'cfg': cfg, 'Env': env}
        return templates['page_file_manager'](**expVars)
