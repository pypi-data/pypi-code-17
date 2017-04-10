#!/usr/bin/env python3
# pylint: disable=singleton-comparison

""" Article type node handler for NodeDispatcher."""

import cherrypy

from ..db import db
from ..models import PageNode


class ArticlelistHandler():
    """Articlelist handler, redirects to its first child node of PageNode type."""

    def __init__(self, node):
        """ unlike regular handlers, NodeDispatcher type ones require
        related SitNode subclass node in the constructor"""
        self.node = node

    @cherrypy.expose
    @cherrypy.tools.require(user_state=True)
    def default(self, *args, **kwargs):  # pylint: disable=unused-argument
        """redirect to its first child node having url"""

        firstChild = db.query(PageNode)\
                       .filter(PageNode.parent == self.node,
                               PageNode.visible == True,
                               PageNode.placement != 'meta')\
                       .order_by(PageNode.position).first()

        if firstChild:
            raise cherrypy.HTTPRedirect(firstChild.url)
        else:
            raise cherrypy.HTTPError(404)
