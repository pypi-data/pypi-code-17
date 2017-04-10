#!/usr/bin/env python3

"""LanguagesV1 handles /_v1/languages/ URL."""

import cherrypy

from ..db import db
from ..models import Language
from ..tools import range_from_header
from .URLHandler import URLHandler


class Languages(URLHandler):
    """handles /_v1/languages/ URL."""

    mount_url = '/_v1/languages'
    dispatcher = 'MethodDispatcher'
    exposed = True

    # pylint: disable=unused-argument,too-many-branches
    @cherrypy.tools.json_out()
    @cherrypy.tools.require()
    def GET(self, langid=None, *, sort=None, attrs=None, **kwargs):
        """produces list of languages supported by site."""

        keys = {'id', 'name', 'native_name', 'long_code', 'iso_code'}
        exports = set(attrs.split(',')) & keys if attrs else keys

        record = lambda c: {k: getattr(c, k) for k in exports}

        if langid is not None:
            if langid.isdecimal():
                c = db.query(Language).get(langid)
            else:
                c = db.query(Language).filter_by(iso_code=langid)

            if c is not None:
                return c.export()
            else:
                raise cherrypy.HTTPError(404, 'Record not found')

        else:
            q = db.query(Language)

            if sort is not None and sort[1:] == 'name':
                if sort[0] != '-':
                    q = q.order_by(Language.name.asc(), Language.iso_code)
                else:
                    q = q.order_by(Language.name.desc(), Language.iso_code)
            elif sort is not None and sort[1:] == 'native_name':
                if sort[0] != '-':
                    q = q.order_by(Language.native_name.asc())
                else:
                    q = q.order_by(Language.native_name.desc())
            elif sort is not None and sort[1:] == 'iso_code':
                if sort[0] != '-':
                    q = q.order_by(Language.iso_code)
                else:
                    q = q.order_by(Language.iso_code.desc())
            else:
                q = q.order_by(Language.native_name, Language.iso_code)

            return [record(c) for c in q[range_from_header(q.count())]]
