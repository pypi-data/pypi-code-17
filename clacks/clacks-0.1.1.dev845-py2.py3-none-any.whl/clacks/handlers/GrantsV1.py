#!/usr/bin/env python3

"""/_v1/grants handler"""


import json

import cherrypy
from sqlalchemy import func

from ..db import db
from ..models import Grant
from ..tools import range_from_header
from .URLHandler import URLHandler


class Grants(URLHandler):

    """/_v1/grants handler"""

    dispatcher = 'MethodDispatcher'
    mount_url = '/_v1/grants'
    exposed = True

    @cherrypy.tools.json_out()
    @cherrypy.tools.require(grant='AUTHORIZED')
    def GET(self, grantid=None, *, internal=False, granted_by=None,
            inject=None, **kwargs):  # pylint: disable=unused-argument

        """Return grants list or grant given."""

        isSystemGrantExpr = func.upper(func.substring(Grant.name, 1, 1)) == func.substring(Grant.name, 1, 1)

        if grantid:
            grant = Grant.get(grantid)
            return {
                'id': grant.name,
                'granted_by': {
                    g: True for g in grant.granted_by
                }
            }
        if inject:
            try:
                extra = [{'id': h[0], 'name': h[1]}
                         for h in (g.split('|')
                                   for g in (d for d in inject.split(';')))]
            except IndexError:
                raise cherrypy.HTTPError(401, 'badly formatted inject parameter')
        else:
            extra = []

        if granted_by:
            grant = Grant.get(granted_by)
            q = db.query(Grant)
            if not internal:
                q = q.filter_by(internal=False)
            q = q.order_by(isSystemGrantExpr, Grant.name)
            return [{'id': g.name,
                     'name': g.name,
                     'granted_by': {granted_by: g.name in grant.grants}}
                    for g in q.http_range()]
        else:
            q = db.query(Grant)
            if not internal:
                q = q.filter_by(internal=False)
            q = q.order_by(isSystemGrantExpr, Grant.name)

            offset = range_from_header(q.count()+len(extra))
            dbOffset = slice(max(0, (offset.start or 0)-len(extra)),
                             None if offset.stop is None else
                             max(0, offset.stop-len(extra)))
            return extra[offset]+[{'id': g.name, 'name': g.name}
                                  for g in q[dbOffset]]

    @cherrypy.tools.json_out()
    @cherrypy.tools.require(grant='SITE_ADMIN')
    def PUT(self, grantid=None, **kwargs):  # pylint: disable=unused-argument

        """Set grant properties"""

        grant = Grant.get(grantid)
        data = json.loads(cherrypy.request.body.read().decode())
        if 'granted_by' in data:
            for k, v in data['granted_by'].items():
                if (k in grant.granted_by) != v:
                    kgrant = Grant.get(k)
                    if v and (kgrant not in grant.allGrants()):
                        grant.granted_by[k] = kgrant
                    elif not v:
                        grant.granted_by.remove(kgrant)
            db.commit()

        return self.GET(grantid)
