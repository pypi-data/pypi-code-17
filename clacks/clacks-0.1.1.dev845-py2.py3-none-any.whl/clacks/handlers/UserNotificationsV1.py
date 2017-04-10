#!/usr/bin/env python3

"""Notifications handler.

   @IDEA: maybe it should be implemented as CherryPy plugin and use messaging?
"""

from datetime import datetime

import cherrypy

from ..tools import range_from_header
from .URLHandler import URLHandler


def notify(group, message):

    """Register a new notification for a user of current session."""
    with cherrypy.session.open('w'):
        if 'notifications' not in cherrypy.session:
            cherrypy.session['notifications'] = []

        cherrypy.session['notifications'].insert(
            0, {'id': datetime.now().isoformat(), 'type': group, 'message': message})

        if len(cherrypy.session['notifications']) > 1000:
            cherrypy.session['notifications'] = cherrypy.session['notifications'][:1000]


class Notifications(URLHandler):

    """Notifications handler."""

    mount_url = '/_v1/user-notifications/'

    @cherrypy.expose
    @cherrypy.tools.require(authorized_user=True)
    @cherrypy.tools.json_out()
    def index(self):
        """Return notifications as requested."""
        with cherrypy.session.open() as session:
            return session.get('notifications', [])[
                range_from_header(len(session.get('notifications')))
            ]

    @cherrypy.expose
    @cherrypy.tools.require(authorized_user=True)
    @cherrypy.tools.json_out()
    def total(self):
        """Return total number of notifications. Probably not needed."""
        with cherrypy.session.open() as session:
            return {'total': len(session.get('notifications', []))}
