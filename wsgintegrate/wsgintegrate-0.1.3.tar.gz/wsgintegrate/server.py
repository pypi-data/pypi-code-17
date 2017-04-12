"""
front-ends for various WSGI servers
"""

from factory import WSGIfactory

__all__ = ['wsgiref', 'servers', 'paster']


### wsgiref

def wsgiref(app, host='0.0.0.0', port=80):
    from wsgiref import simple_server
    server = simple_server.make_server(host=host, port=int(port), app=app)
    server.serve_forever()

servers = {'wsgiref': wsgiref}


### paste

try:
    from paste import httpserver
    def paste_server(app, host='0.0.0.0', port=80):
        httpserver.serve(app, host=host, port=port)
    servers['paste'] = paste_server
except ImportError:
    print ("Not adding paste.httpserver; not installed")

def paster(global_conf, **kw):
    """factory for paster"""
    return WSGIfactory(**kw)


### tornado
### http://www.tornadoweb.org/en/stable/httpserver.html
### http://www.tornadoweb.org/en/stable/httputil.html#tornado.httputil.HTTPServerRequest
### unfinished

try:

    import tornado.httpserver
    import tornado.ioloop

    def handle_request(request):
        message = "You requested %s\n" % request.uri
        request.connection.write_headers(
            httputil.ResponseStartLine('HTTP/1.1', 200, 'OK'),
            {"Content-Length": str(len(message))})
        request.connection.write(message)
        request.connection.finish()
#http_server = tornado.httpserver.HTTPServer(handle_request)
#http_server.listen(8888)
#tornado.ioloop.IOLoop.instance().start()
except ImportError:
    pass
