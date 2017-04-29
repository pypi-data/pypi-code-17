import string
import os
import cgi

from PTMLRequest import PTMLRequest

class CGIRequest(PTMLRequest):

    def __init__(this):
        this.params = cgi.FieldStorage()


    def getHeader(this, name):
        name = "HTTP_" + string.upper(name)
        return os.environ[name]


    def hasHeader(this, name):
        name = "HTTP_" + string.upper(name)
        return os.environ.has_key(name)


    def getPathInfo(this):
        if os.environ.has_key("PATH_INFO"):
            return os.environ["PATH_INFO"]
        else:
            return None


    def getRequestURI(this):
        return os.environ["REQUEST_URI"]


    def getQueryString(this):
        if os.environ.has_key("QUERY_STRING"):
            return os.environ["QUERY_STRING"]
        else:
            return None


    def getRemoteAddress(this):
        if os.environ.has_key("REMOTE_ADDR"):
            return os.environ["REMOTE_ADDR"]
        else:
            return None

    def getRemotePort(this):
        if os.environ.has_key("REMOTE_PORT"):
            return os.environ["REMOTE_PORT"]
        else:
            return None

    def getRequestMethod(this):
        if os.environ.has_key("REQUEST_METHOD"):
            return os.environ["REQUEST_METHOD"]
        else:
            return None

    def getParam(this, name):
        if not this.params.has_key(name):
            return cgi.MiniFieldStorage(name, None)

        return this.params[name]


    def hasParam(this, name):
        return this.params.has_key(name)


    def getParamNames(this):
        return this.params.keys()

# vim: set et sts=4 sw=4 :
