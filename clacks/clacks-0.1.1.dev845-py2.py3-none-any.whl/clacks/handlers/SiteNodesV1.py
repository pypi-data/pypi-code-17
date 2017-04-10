#!/usr/bin/env python3

# WARNING: changes to this file need to be cloned
# to SiteNodesV1Versioned from ext.versioning to keep it in sync
# until better solution is found


"""/_v1/site-nodes/ handler."""

import json
import sys

import cherrypy
from sqlalchemy.orm import undefer

from ..core import cfg
from ..db import db
from ..gettext import gettext as _
from ..models import HeadNode, SiteNode
from ..tools import range_from_header
from .URLHandler import URLHandler


class SiteNodes(URLHandler):

    """/_v1/site-nodes/ handler."""

    dispatcher = 'MethodDispatcher'
    mount_url = '/_v1/site-nodes'
    exposed = True

    @cherrypy.tools.json_out()
    @cherrypy.tools.require(grant='SITE_STRUCTURE_VIEW')
    def GET(self, node_id=None, **kwargs):

        """Return requested nodes."""

        def exportNode(node):
            """JSON friendly dictionary with node common essential data"""
            return {
                'id': node.id,
                '_parent': node._parent,
                'linkName': node.linkName,
                'position': node.position,
                'visible': node.visible,
                'viewGranted': node.viewGranted(cherrypy.request.user),
                'editGranted': node.editGranted(cherrypy.request.user),
                'addNodeGranted': node.addNodeGranted(cherrypy.request.user),
                'lang': node.lang,
                'type': node.type,
                'placement': node.placement,
                'childNodesCount': node.childNodesCount
            }

        if node_id is not None:
            node = db.query(SiteNode).get(node_id)
            if node:
                result = exportNode(node)
                result.update(node.export())
                return result
            else:
                raise cherrypy.HTTPError(404, 'Record not found')

        if 'parent' in kwargs:
            if kwargs.get('parent', None) in {None, 'head'}:
                parent = HeadNode.get()
            else:
                parent = (db.query(SiteNode).options(undefer(SiteNode.childNodesCount))
                          .get(kwargs['parent']))

            query = (parent.childNodesQuery
                     .options(undefer(SiteNode.childNodesCount)))
        else:
            query = (db.query(SiteNode)
                     .options(undefer(SiteNode.childNodesCount))
                     .order_by(SiteNode.id))

        return [exportNode(node) for node in query[range_from_header(query.count())]]

    @cherrypy.tools.json_out()
    @cherrypy.tools.require(grant='SITE_STRUCTURE_VIEW')
    def PUT(self, node_id):

        """Update node data."""

        node_id = int(node_id)
        data = json.loads(cherrypy.request.body.read().decode())

        if node_id != int(data['id']):
            raise cherrypy.HTTPError(400, _("Link id from URL doesn't match JSON one"))

        node = db.query(SiteNode).get(node_id)

        if not cherrypy.request.user.granted('SITE_ADMIN'):
            data.pop('viewGrant', None)
            data.pop('editGrant', None)
            data.pop('addNodeGrant', None)

        if node.editGranted(cherrypy.request.user):
            node.update(data)
        else:
            raise cherrypy.HTTPError(403, _("You aren't granted to make this edition"))
        db.commit()

        return self.GET(node_id)

    @cherrypy.tools.json_out()
    @cherrypy.tools.require(grant='SITE_STRUCTURE_VIEW')
    def POST(self):
        """Create a new node"""

        data = json.loads(cherrypy.request.body.read().decode())
        parent = db.query(SiteNode).get(data['_parent'])

        if not cherrypy.request.user.granted('SITE_ADMIN'):
            data.pop('viewGrant', None)
            data.pop('editGrant', None)
            data.pop('addNodeGrant', None)

        if not parent.addNodeGranted(cherrypy.request.user):
            raise cherrypy.HTTPError(403, _("You aren't granted to add  a new item here"))

        if 'template' in data:
            fdata = cfg.get('page', 'factory',
                            data['template'].split(':')[0], default=None)
            if not fdata:
                raise cherrypy.HTTPError(400, _("Bad request"))

            __import__(fdata['module'])

            factory = getattr(sys.modules[fdata['module']],
                              fdata['factory'])
            position = 0 if cherrypy.request.headers.get('Put-Default-Position', 'end') == 'start' else None
            newnode = factory.create(parent, data['template'],
                                     data['linkName'],
                                     position)
            db.commit()

            return self.GET(newnode.id)

        raise NotImplementedError('<html>%r</html>' % vars())

    @cherrypy.tools.json_out()
    @cherrypy.tools.require(grant='SITE_STRUCTURE_VIEW')
    def DELETE(self, node_id):
        """Drop node if it doesn't have children."""
        node = db.query(SiteNode).get(node_id)
        if node.childNodesCount == 0:
            node.delete()
            db.commit()
            cherrypy.response.status = "204 Removed"
            return {}
