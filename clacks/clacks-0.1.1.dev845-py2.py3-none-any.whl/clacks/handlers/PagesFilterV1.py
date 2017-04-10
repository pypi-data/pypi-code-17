#!/usr/bin/env python3

""" AdminSiteNodes handler """

import cherrypy

from ..db import db
from ..gettext import gettext as _
from ..models import PageNode, SiteNode
from .URLHandler import URLHandler


class AdminPagesFilter(URLHandler):
    """This service is read only returns link names in two forms basic and additional
    containing parent link name and current page position to ease page identification
    """

    dispatcher = 'MethodDispatcher'
    mount_url = '/_v1/pages-filter'
    exposed = True

    @cherrypy.tools.json_out()
    @cherrypy.tools.require(grant='SITE_STRUCTURE_VIEW')
    def GET(self, node_id=None, *, linkName=None, **kwargs):

        """Useful for filtering selects."""

        queryNode = SiteNode

        if 'type' in kwargs:
            if kwargs['type'] == 'page':
                queryNode = PageNode

        if node_id:
            node = db.query(queryNode).get(node_id)
            if not node:
                raise cherrypy.HTTPError(404, _('Not found'))
            return {'id': node.id, 'linkName': node.linkName}

        nodes = db.query(queryNode)

        if linkName is not None:
            if linkName[-1:] == '*':
                nodes = nodes.filter(queryNode.linkName.ilike('%'+linkName[:-1]+'%'))
            else:
                nodes = nodes.filter(queryNode.linkName == linkName)

        nodes = nodes.order_by(queryNode.linkName, queryNode.id)

        return [{'id': n.id,
                 'linkName': n.linkName,
                 'fullName': _('{} (pos. {} in “{}”)').format(
                     n.linkNameCut(48), n.position+1,
                     n.parent.linkNameCut(32) if n.parent else _('[top]'))}
                for n in nodes.all()]
