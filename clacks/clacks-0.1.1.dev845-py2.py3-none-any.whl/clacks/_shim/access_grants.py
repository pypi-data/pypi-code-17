#!/usr/bin/env python3

"""
In your application configuration add:

[/]
tools.force_require.on = True

"""

import cherrypy


def _require(grant=None, any_grant=None, authorized_user=False, user_state=False):
    """CherryPy Tool that decorates methods with user grants required
       for them to be available for user"""
    from ..db import db
    from ..models import User

    if any_grant is None:
        any_grant = []

    if grant or any_grant or authorized_user or user_state:

        with cherrypy.session.open():
            uid = cherrypy.session.get('admin-user', None)
        user = db.query(User).get(uid) if uid else None
        cherrypy.request.user = user

        if grant and not (user and user.granted(grant)):
            raise cherrypy.HTTPError(401, 'Unauthorized')

        if any_grant and not (user and user.grantedAny(any_grant)):
            raise cherrypy.HTTPError(401, 'Unauthorized')

        if authorized_user and not user:
            raise cherrypy.HTTPError(401, 'Unauthorized')
    else:
        cherrypy.request.user = None


def _force_require():
    """CherryPy Tool that forces setting grant requirement
       on any publicly accessible method. """

    if not hasattr(cherrypy.request, 'user'):
        raise cherrypy.HTTPError(message="Access rights not implemented for %r" %
                                 cherrypy.request.handler.oldhandler)


cherrypy.tools.require = cherrypy.Tool('before_handler', _require, priority=97)
cherrypy.tools.force_require = cherrypy.Tool('before_handler', _force_require, priority=98)
