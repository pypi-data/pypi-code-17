
import os.path
import cgi
import traceback
import sys
import string
import cStringIO

import BaseHTTPServer

from ptml.PTMLResponse import PTMLResponse
from ptml.PyHTTPDRequest import PyHTTPDRequest
from ptml.Exceptions import *

class PTMLHTTPServer(BaseHTTPServer.HTTPServer):

    def __init__(this, addr, autoparser, handler):
        BaseHTTPServer.HTTPServer.__init__(this, addr, handler)
        this.autoparser = autoparser



class PTMLHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    extensions_map = {
        ".html":    "text/html",
        ".htm":     "text/html",
        ".ptml":    "text/html",
        ".gif":     "image/gif",
        ".jpeg":    "image/jpeg",
        ".jpg":     "image/jpeg"
    }

    def do_POST(this):
        return this.do_GET()


    def do_GET(this):

        resp = PTMLResponse()
        req = PyHTTPDRequest(this)
        buf = cStringIO.StringIO()

        try:
            oldstdout = sys.stdout
            sys.stdout = buf

            cache = this.server.autoparser.handleRequest(req.getRequestURI())

            try:
                execfile(cache,
                    {"stdout": buf, "response": resp, "request": req})
            except SystemExit, code:
                pass

            sys.stdout = oldstdout
            headers = resp.getHeaders()

            status = -1
            content_type = -1

            for k in headers.keys():
                if string.lower(k) == "status":
                    status = headers[k]
                if string.lower(k) == "content-type":
                    content_type = 1

            if status == -1:
                status = "200"

            if content_type == -1:
                headers["Content-type"] = "text/html"

            this.send_response(status)

            for k in headers.keys():
                this.send_header(k, headers[k])

            this.end_headers()

            this.wfile.write(buf.getvalue())

        except FileNotFoundException:
            this.send_response(404)
            this.send_header("Content-type", "text/html")
            this.end_headers()

            this.wfile.write(
                "<html><head><title>404 Not Found</title></head><body>\n")
            this.wfile.write("<h1>Not Found</h1>\n")
            this.wfile.write(
                "The requested URL " + cgi.escape(req.getRequestURI()) +
                " was not found on this server.<p>\n")
            this.wfile.write(
                "<hr><address>%s</address>\n" % this.server_version)
            this.wfile.write("</body></html>\n")

        except:
            this.send_response(500)
            this.send_header("Content-type", "text/html")
            this.end_headers()

            lines = apply(traceback.format_exception, sys.exc_info())
            this.wfile.write("<html><body>\n<h1>Fatal Exception</h1>\n<pre>\n")
            this.wfile.write(cgi.escape(string.join(lines)))
            this.wfile.write("</pre>\n</body></html>\n")

    def guess_type(this, path):

        (base, ext) = os.path.splitext(string.lower(path))

        if this.extensions_map.has_key(ext):
            return this.extensions_map[ext]
        else:
            return "text/html"

# vim: set et sts=4 sw=4 :
