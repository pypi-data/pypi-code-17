from jackster.funcs import chain, stop, status
from jackster.errors import defaultErrors

import werkzeug
from werkzeug.serving import run_simple

import json
import re
from traceback import print_tb

class Request(werkzeug.wrappers.Request):
    pass

class Response(werkzeug.wrappers.Response):
    def get_status(self):
        return self.status_code
    def set_status(self, status):
        self.status_code = status
        return self
    def get_body(self):
        return self.get_data(True)
    def set_body(self, body):
        self.set_data(body)
        return self
    def get_content_type(self):
        return  self.content_type
    def set_content_type(self, content_type):
        self.content_type = content_type
        return self
    def html(self, html):
        return self.set_content_type('text/html').set_body(html)
    def json(self, obj):
        return self.set_content_type('application/json').set_body(json.dumps(obj))
    def text(self, text):
        return self.set_content_type('text/plain').set_body(text)

class Router:
    """ Provides Routing for application logic. """
    def __init__(self, name=None):
        self.name, self.handlers = name, []
    # Methods to add handlers for every http request method
    def options(self, path, handler=r'^$', name=None):
        return self.method('OPTIONS', path, handler, name)
    def get(self, path, handler=r'^$', name=None):
        return self.method('GET', path, handler, name)
    def head(self, path, handler=r'^$', name=None):
        return self.method('HEAD', path, handler, name)
    def post(self, path, handler=r'^$', name=None):
        return self.method('POST', path, handler, name)
    def put(self, path, handler=r'^$', name=None):
        return self.method('PUT', path, handler, name)
    def patch(self, path, handler=r'^$', name=None):
        return self.method('PATCH', path, handler, name)
    def delete(self, path, handler=r'^$', name=None):
        return self.method('DELETE', path, handler, name)
    def trace(self, path, handler=r'^$', name=None):
        return self.method('TRACE', path, handler, name)
    def connect(self, path, handler=r'^$', name=None):
        return self.method('CONNECT', path, handler, name)
    # Methods to add handlers for errors
    def error(self, code, path, handler=r'^$', name=None):
        return self.method(code, path, [status(code), handler], name)
    # Method to add handlers that will be used for every method
    def use(self, path, handler=r'^', name=None):
        return self.method('USE', path, handler, name)
    # Shortcut for creating a subrouter
    def route(self, path, name=None):
        router = Router(name)
        self.method('USE', path, router)
        return router
    # General method for adding a method
    def method(self, method, path, handler=r'^$', name=None):
        if isinstance(method, (list, tuple)):
            for m in method:
                self.method(m, path, handler)
            return self
        if isinstance(handler, str):
            self.handlers.append((method, re.compile(handler), path))
            return self
        if method == 'USE' and isinstance(handler, Router):
            self.handlers.append((method, re.compile(path), handler))
            return self
        self.handlers.append(('USE', re.compile(path), Router(name).method(method, handler)))
        return self
    # Try to match a method and path to this router
    def match(self, method, path):
        handlers, args, kwargs = [], (), {}
        found, exists = False, False
        for method_, path_, handler in self.handlers:
            match = path_.search(path)
            if match and (method_ == method or method_ == 'USE'):
                if method_ != 'USE':
                    found, exists = True, True
                if isinstance(handler, Router):
                    handlers_, args_, kwargs_ = handler.match(method, path[:match.start()] + path[match.end():])
                    if handlers_ is not None:
                        exists = True
                        if handlers_ != []:
                            found = True
                            handlers += handlers_
                            args += match.groups() + args_
                            kwargs = {**kwargs, **match.groupdict(), **kwargs_}
                else:
                    handlers.append(handler)
                    args += match.groups()
                    kwargs = {**kwargs, **match.groupdict()}
            elif match and not isinstance(method_, int):
                exists = True
        return ((handlers if found else []) if exists else None), args, kwargs
    # Start a server from this router
    def listen(self, host='localhost', port=8000):
        run_simple(host, port, self, use_reloader=True)
    # Turns a Request object into a Response object according to how this app is defined
    @Request.application
    def __call__(self, req):
        handler, args, kwargs = self.match(req.method, req.path.rstrip('/'))
        # Check for 404 errors
        if handler is None:
            handler, args, kwargs = self.match(404, req.path)
            if handler is None:
                handler, args, kwargs = defaultErrors[404], (), {}
        # Check for 405 errors
        if handler == []:
            handler, args, kwargs = self.match(405, req.path)
            if handler == []:
                handler, args, kwargs = defaultErrors[405], (), {}
        req.path_args, req.path_kwargs, req.app = args, kwargs, self
        res = Response()
        # Check for 500 errors
        try:
            chain(handler, stop)(req, res, None)
        except Exception as e:
            print_tb(e.__traceback__)
            print(e.__class__.__name__ + ': ' + str(e))
            handler, args, kwargs = self.match(500, req.path)
            if handler is None or handler == []:
                handler, args, kwargs = defaultErrors[500], (), {}
            res = Response()
            # Check for 500 error in user defined error handling
            try:
                chain(handler, stop)(req, res, None, e)
            except Exception as e:
                handler, args, kwargs = defaultErrors[500], (), {}
                res = Response()
                chain(handler, stop)(req, res, None, e)
        return res
