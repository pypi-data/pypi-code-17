#!/usr/bin/env python3

"""AdminGrantUsers handler."""

import json

import cherrypy

from ..db import db
from ..gettext import gettext as _
from ..models import Grant, User
from ..tools import range_from_header
from .URLHandler import URLHandler


class UserGrants(URLHandler):

    """AdminGrantUsers handler."""

    mount_url = '/_v1/user-grants/'
    dispatcher = 'MethodDispatcher'
    exposed = True

    @cherrypy.tools.require(grant='SITE_ADMIN')
    @cherrypy.tools.json_out()
    def GET(self, userid=None, grantid=None,  # pylint: disable=unused-argument
            *, grant=None, **kwargs):

        """Return full list of users with informations about grant given."""

        if not (userid and grantid or grant):
            raise cherrypy.HTTPError(400, _('Either …/[uid] or ?grant=… filter expected'))

        if userid:
            user = db.query(User).get(userid)
            if not user:
                raise cherrypy.HTTPError(404, _('User of given id not found'))

            grant = db.query(Grant).get(grantid)
            if not grant:
                raise cherrypy.HTTPError(404, _('Grant of given id not found'))
            return {'id': '/'.join([str(user.id), str(grant.id)]),
                    'login': user.login,
                    'granted': user.granted(grant),
                    'directly': user.isDirectGrant(grant)}

        grant = Grant.get(grant)
        if not grant:
            raise cherrypy.HTTPError(404, _('Given grant name not found'))

        q = db.query(User).order_by(User.login)

        return [{'id': '/'.join([str(u.id), str(grant.id)]),
                 'login': u.login,
                 'granted': u.granted(grant),
                 'directly': u.isDirectGrant(grant)}
                for u in q[range_from_header(q.count())]]

    @cherrypy.tools.require(grant='SITE_ADMIN')
    @cherrypy.tools.json_out()
    def PUT(self, userid, grantid):
        """update grant to user assignment status"""

        data = json.loads(cherrypy.request.body.read().decode())
        user = db.query(User).get(userid)
        if not user:
            raise cherrypy.HTTPError(404, _('User of given id not found'))

        grant = db.query(Grant).get(grantid)
        if not grant:
            raise cherrypy.HTTPError(404, _('Grant of given id not found'))

        if data['directly']:
            user.setGrant(grant)
        else:
            user.dropGrant(grant)
        db.commit()

        return self.GET(userid, grantid)
