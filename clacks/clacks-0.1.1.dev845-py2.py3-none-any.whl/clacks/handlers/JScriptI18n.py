#!/usr/bin/env python3

"""Translations handler"""

import re

import cherrypy

from ..core import ROOTPATH
from ..i18n.mo2json import convert
from .URLHandler import URLHandler


class JScriptI18n(URLHandler):

    """Translations handler"""

    mount_url = '/_js/i18n/'

    @cherrypy.expose
    @cherrypy.tools.require()
    def default(self, lang):

        """Return gettext translation as JSON dictionary"""

        if not re.match('^[a-z]{2}.json$', lang):
            raise cherrypy.HTTPError(404)

        lang = lang[:2]

        result = convert('jscript', str(ROOTPATH/'locale'), [lang], True)

        with (ROOTPATH/('http/_js/i18n/%s.json' % lang)).open('w') as f:
            f.write(result)

        return result
