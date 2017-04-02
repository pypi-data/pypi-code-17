import json

import aiohttp.web

from asynclib.http.parser import error_middleware


class RestServer(object):
    def __init__(self, name):
        self.name = name
        self.app = aiohttp.web.Application(middlewares=[error_middleware])
        self.app.router.add_get('/{}/heartbeat'.format(self.name), self.heartbeat)

    def add_resource(self, path, resource):
        for method in ['get', 'put', 'post', 'delete', 'patch']:
            if hasattr(resource, method):
                self.app.router.add_route(method.upper(), '/{}{}'.format(self.name, path), getattr(resource, method))

    def add_handler(self, path, method, handler):
        self.app.router.add_route(method, '/{}{}'.format(self.name, path), handler)

    async def heartbeat(self, request):
        return aiohttp.web.Response(body=json.dumps({'alive': True}), status=200, content_type='application/json')

    def run(self, host, port, loop):
        aiohttp.web.run_app(self.app, host=host, port=port, loop=loop)
