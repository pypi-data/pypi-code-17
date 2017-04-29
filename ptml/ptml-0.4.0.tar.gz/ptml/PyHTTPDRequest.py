import string
import cgi

from PTMLRequest import PTMLRequest

class PyHTTPDRequest(PTMLRequest):

    def __init__(this, req):
        this.req = req

        environ = {}

        environ["REQUEST_METHOD"] = this.getRequestMethod()

        if this.getQueryString() is not None:
            environ["QUERY_STRING"] = this.getQueryString()

        if this.hasHeader("Content-type"):
            environ["CONTENT_TYPE"] = this.getHeader("Content-type")

        if this.hasHeader("Content-length"):
            environ["CONTENT_LENGTH"] = this.getHeader("Content-length")

        this.params = cgi.FieldStorage(fp = this.req.rfile, environ = environ)


    def getHeader(this, name):
        return this.req.headers[name]


    def hasHeader(this, name):
        return this.req.headers.has_key(name)


    def getRequestURI(this):
        path = this.req.path
        q = string.find(path, "?")
        if q > 0:
            return path[:q]
        else:
            return path


    def getPathInfo(this):
        return None


    def getQueryString(this):
        path = this.req.path
        q = string.find(path, "?")
        if q > 0:
            return path[q + 1:]
        else:
            return None


    def getRemoteAddress(this):
        return this.req.client_address[0]


    def getRemotePort(this):
        return this.req.client_address[1]


    def getRequestMethod(this):
        return this.req.command


    def getParam(this, name):
        if not this.params.has_key(name):
            return cgi.MiniFieldStorage(name, None)

        return this.params[name]


    def hasParam(this, name):
        return this.params.has_key(name)


    def getParamNames(this):
        return this.params.keys()

# vim: set et sts=4 sw=4 :
