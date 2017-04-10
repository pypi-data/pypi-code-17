#!/usr/bin/env python3

"""ControlsV1 handles /_v1/controls/ URL."""

import json

import cherrypy

from ..db import db
from ..models import ArticleNode, Control, SiteNode
from .URLHandler import URLHandler


class Controls(URLHandler):
    """handles /_v1/controls/ URL."""

    mount_url = '/_v1/controls'
    dispatcher = 'MethodDispatcher'
    exposed = True

    @cherrypy.tools.json_out()
    @cherrypy.tools.require(grant='SITE_STRUCTURE_VIEW')
    def GET(self, cid=None, *, sitenode=None, **kwargs):  # pylint: disable=unused-argument
        """Get constrols support"""

        if cid is not None:
            return db.query(Control).get(int(cid)).export()

        inject = []
        q = db.query(Control)

        if sitenode:
            node = db.query(SiteNode).get(sitenode)
            q = q.filter(Control._page == node.id)
            if isinstance(node, ArticleNode):
                inject = [{
                    'id': 0,
                    'name': 'Artykuł',
                    '_priority': -1,
                    'dynamic': False,
                    'enabled': True,
                    'placement': 'body',
                    '_class': 'article',
                    '_page': node.id
                }]

        q = q.order_by(Control._page, Control._priority)

        return inject+[c.export() for c in q.all()]
        # code below cannot be used due to injection of additional 'article' pseudo control:
        # return [c.export() for c in q[range_from_header(q.count())]]

    @cherrypy.tools.json_out()
    @cherrypy.tools.require(grant='SITE_STRUCTURE_VIEW')
    def POST(self):
        """Create control."""
        import gtcms.models as models

        data = json.loads(cherrypy.request.body.read().decode())

        if 'type' in data:
            Ctrl = getattr(models, data['type']+'Control')
            node = db.query(SiteNode).get(int(data['_page']))
            control = Ctrl(page=node, placement=data.pop('placement'))
            db.add(control)
            db.flush()
            control.update(data)
            db.commit()
            return self.GET(control.id)
        else:
            raise cherrypy.HTTPError(400, 'Bad request')

    @cherrypy.tools.json_out()
    @cherrypy.tools.require(grant='SITE_STRUCTURE_VIEW')
    def PUT(self, ctrlid):
        """Update control, supports reordering."""

        ctrl = db.query(Control).get(ctrlid)

        data = json.loads(cherrypy.request.body.read().decode())

        if 'Put-Before' in cherrypy.request.headers:
            refctrl = db.query(Control).get(cherrypy.request.headers['Put-Before'])
            if (refctrl == ctrl) or (ctrl.page != refctrl.page):
                raise cherrypy.HTTPError(400, 'Bad request')
            page = ctrl.page
            page.controls.remove(ctrl)
            page.controls.insert(refctrl._priority-(refctrl._priority > ctrl._priority), ctrl)
        elif 'Put-Default-Position' in cherrypy.request.headers:
            page = ctrl.page
            page.controls.remove(ctrl)
            if cherrypy.request.headers['Put-Default-Position'] == 'end':
                page.controls.append(ctrl)
            elif cherrypy.request.headers['Put-Default-Position'] == 'start':
                page.controls.insert(0, ctrl)
            else:
                raise cherrypy.HTTPError(400, 'Bad request')

        ctrl.update(data)
        db.commit()

        return self.GET(ctrlid)

    @cherrypy.tools.json_out()
    @cherrypy.tools.require(grant='SITE_STRUCTURE_VIEW')
    def DELETE(self, ctrlid):
        """Delete control."""

        ctrl = db.query(Control).get(int(ctrlid))
        ctrl.delete()
        db.commit()
        cherrypy.response.status = "204 Removed"
        return {}
