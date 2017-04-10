#!/usr/bin/env python3

""" client login form """

import cherrypy

from ..core.templates import templates
from ..tools import structural
from .Component import Component


class cClientLogin(Component):
    """ client login form """

    def __init__(self, placement):
        """default placement is set here."""
        super().__init__()
        self._placement = placement

    @structural
    def fetch(self, placement):    # pylint: disable=unused-argument
        """return html content."""
        body = templates['form_logged_in' if cherrypy.request.user else 'form_login']
        return body(user=cherrypy.request.user)
