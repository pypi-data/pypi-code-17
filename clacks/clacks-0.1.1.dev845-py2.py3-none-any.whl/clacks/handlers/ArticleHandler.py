#!/usr/bin/env python3

""" Article type node handler for NodeDispatcher."""

import cherrypy

from ..core.CPage import CPage
from ..core.templates import templates
from ..core.url import Url
from ..db import db
from ..gettext import gettext as _
from ..models import ControlProperty, PageNode, RestrictedAccessControl
from ..tools import structural


class ArticleHandler():
    """Session authentication state handler."""

    def __init__(self, node):
        """Unlike regular handlers, NodeDispatcher type ones require
        related SitNode subclass node in the constructor"""
        self.node = node

    @cherrypy.expose
    @cherrypy.tools.require(user_state=True)
    def default(self, *args, **kwargs):  # pylint: disable=unused-argument
        """Wrap article content into page template and serve it."""

        if kwargs.get('__print__', None):
            cherrypy.request.printMode = True

        if any('.' not in s for s in args):
            raise cherrypy.HTTPError(404)

        cherrypy.request.url = Url()

        if not self.node.viewGranted(cherrypy.request.user) and \
           not getattr(cherrypy.request, 'printMode', False):
            target = db.query(RestrictedAccessControl)\
                       .join(ControlProperty, PageNode)\
                       .filter(ControlProperty.name == 'landing_page',
                               ControlProperty.value == 'true',
                               PageNode.lang == self.node.lang)\
                       .first()
            if target and not cherrypy.request.user:
                raise cherrypy.HTTPRedirect(target.page.url+'?ref='+str(self.node.id))
            else:
                raise cherrypy.HTTPError(
                    403, _("Sorry, you are not permitted to visit this page."))

        page = CPage(node=self.node)

        page.placeElement(self, 'body')
        return page.fetch()

    @structural
    def fetch(self, placement):  # pylint: disable=unused-argument
        """return article body """
        return templates['body_article'](node=self.node, this=self.node)
