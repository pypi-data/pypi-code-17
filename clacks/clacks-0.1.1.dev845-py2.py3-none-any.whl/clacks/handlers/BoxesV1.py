#!/usr/bin/env python3

"""BoxesV1 handles /_v1/boxes/ URL."""

import json

import cherrypy

from ..db import db
from ..models import Box
from ..tools import range_from_header

from .URLHandler import URLHandler


class Boxes(URLHandler):
    """handles /_v1/boxes/ URL."""

    mount_url = '/_v1/boxes'
    dispatcher = 'MethodDispatcher'
    exposed = True

    @cherrypy.tools.json_out()
    @cherrypy.tools.require(any_grant=['SITE_TREE_VIEW'])
    def GET(self, bid=None, *, sort=None, attrs=None, **kwargs):  # pylint: disable=unused-argument
        """produce boxes list with json compatible content."""

        keys = set(['id', 'label', 'title', 'content', 'lang'])
        exports = set(attrs.split(',')) & keys if attrs else keys

        record = lambda c: {k: getattr(c, k) for k in exports}  # nopep8

        if bid is not None:
            c = db.query(Box).get(bid)

            if c is not None:
                return record(c)
            else:
                raise cherrypy.HTTPError(404, 'Record not found')

        else:
            q = db.query(Box)

            # if 'filter' in kwargs:
            #     s = kwargs.pop('filter')

            #     if s[-1:] == '*':
            #         s = s[:-1]+'%'
            #         if s[:1] == '*':
            #             s = '%'+s[1:]

            #     q = q.filter(User.login.concat(' ')
            #                  .concat(User.name).concat(' ')
            #                  .concat(User.surname)
            #                  .concat(' ')
            #                  .concat(func.coalesce(User.company, ''))
            #                  .concat(' ')
            #                  .concat(User.email)
            #                  .ilike(s))

            if sort is not None and sort[1:] == 'label':
                if sort[0] != '-':
                    q = q.order_by(Box.label.asc(), Box.id)
                else:
                    q = q.order_by(Box.label.desc(), Box.id)
            elif sort is not None and sort[1:] == 'title':
                if sort[0] != '-':
                    q = q.order_by(Box.title.asc(), Box.id)
                else:
                    q = q.order_by(Box.title.desc(), Box.id)
            return [record(c) for c in q[range_from_header(q.count())]]

    @cherrypy.tools.json_out()
    @cherrypy.tools.require(grant='SITE_TREE_VIEW')
    def PUT(self, bid=None):  # pylint: disable=too-many-locals,too-many-branches
        """Update Box data"""

        data = json.loads(cherrypy.request.body.read().decode())

        if bid is None or not bid.isdecimal() or int(bid) != data['id']:
            cherrypy.HTTPError(400, 'Bad syntax')

        box = db.query(Box).get(data['id'])

        if 'label' in data and not len(data['label']):
            cherrypy.HTTPError(400, 'Empty label field not allowed')

        for field in ['label', 'title', 'content']:
            if field in data:
                setattr(box, field, data[field])

        db.commit()

        return self.GET(bid)

    @cherrypy.tools.json_out()
    @cherrypy.tools.require(grant='SITE_TREE_VIEW')
    def POST(self):
        """Create a new Box content"""

        data = json.loads(cherrypy.request.body.read().decode())

        if 'id' in data:
            cherrypy.HTTPError(400, 'Bad request')

        box = Box()

        if 'label' not in data or not len(data['label']):
            cherrypy.HTTPError(400, 'Empty label field not allowed')

        if 'label' not in data or not len(data['lang']):
            cherrypy.HTTPError(400, 'Empty lang field not allowed')

        for field in ['label', 'title', 'content', 'lang']:
            if field in data:
                setattr(box, field, data[field])

        db.add(box)
        db.commit()

        return self.GET(box.id)

    @cherrypy.tools.json_out()
    @cherrypy.tools.require(grant='SITE_STRUCTURE_VIEW')
    def DELETE(self, node_id):
        """Drop node if it doesn't have children."""
        node = db.query(Box).get(node_id)
        if node:
            db.delete(node)
            db.commit()
            cherrypy.response.status = "204 Removed"
            return []
