#!/usr/bin/env python3

"""
UserService module for getting user related info.

CurrenUserService class handles /_rest/user/current/url namespace

TODO: current implementation hardcodes values and their sources.
Final one needs to have configurable data providers (or other mechanism
of managing optional data sources)

WARNING: despite placed in core.cms this module depends on core.shop
model classes for now - needs to be rebuilt to optional functionality.
"""

import cherrypy

from .URLHandler import URLHandler


class RestUserCurrent(URLHandler):

    """CurrenUserService class handles /_rest/user/current/url namespace"""

    mount_url = '/_rest/user/current'

    @cherrypy.expose
    @cherrypy.tools.require(authorized_user=True)
    @cherrypy.tools.json_out()
    def wallet(self):
        """Wallet state of current user if available"""

        return {'balance': float(cherrypy.request.user.wallets[0].balance),
                'currency': cherrypy.request.user.wallets[0].currency}

    @cherrypy.expose
    @cherrypy.tools.require(authorized_user=True)
    @cherrypy.tools.json_out()
    def index(self):
        """Should return details about currently logged in user (or anonymous if applicable)"""

        raise cherrypy.HTTPError(501, 'Not yet implemented')
