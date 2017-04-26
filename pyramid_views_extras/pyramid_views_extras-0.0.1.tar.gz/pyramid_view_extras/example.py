#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid_view_extras import class_view_config


class Resource(object):
    allowed_options = ('get',)

    def get(self, context, request):
        return Response('Hello, world !')


@class_view_config(route_name='index_class')
class DecoratedResource(object):
    allowed_options = ('get',)

    def get(self, context, request):
        return Response('Decorated class view')


if __name__ == '__main__':
    config = Configurator()
    config.include('pyramid_view_extras')
    config.add_route('index', '/1')
    config.add_route('index_class', '/2')
    config.add_class_view(Resource, route_name='index')
    config.scan('.')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
