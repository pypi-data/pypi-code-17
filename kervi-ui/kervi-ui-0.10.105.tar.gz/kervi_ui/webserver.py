# Copyright (c) 2016, Tim Wentzlau
# Licensed under MIT

""" Simple web server for the Kervi application """
import os
import time
from socketserver import ThreadingMixIn
import http.client
from kervi.spine import Spine

try:
    from SimpleHTTPServer import SimpleHTTPRequestHandler
except:
    from http.server import SimpleHTTPRequestHandler

try:
    from BaseHTTPServer import HTTPServer
except:
    from http.server import HTTPServer

import socket
import threading
import kervi_ui
import os

class _HTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, req, client_addr, server):
        try:
            SimpleHTTPRequestHandler.__init__(self, req, client_addr, server)
            self.server = server
            self.req = req
        except socket.error:
            pass

    def log_message(self, format, *args):
        return

    def do_GET(self):
        try:
            if self.path.startswith("/cam"):
                path = self.path.split("/")
                cam_id = path[-1]
                spine = Spine()
                print("cam:", cam_id)
                info = spine.send_query("getComponentInfo", cam_id)
                if info:
                    conn = http.client.HTTPConnection(info["ui"]["source"]["server"], timeout=self.timeout)
                    conn.request("GET", info["ui"]["source"]["path"])
                    res = conn.getresponse()
                    self.send_response(res.status)
                    for line in res.headers:
                        self.send_header(line, res.headers[line])
                    self.end_headers()
                    while not self.server.terminate:
                        chunk = res.read(8192)
                        if not chunk:
                            break
                        self.wfile.write(chunk)
            elif self.path.endswith("global.js"):
                self.send_response(200)
                self.send_header('Content-type', 'text/javascript')
                self.end_headers()
                response = bytes("kerviSocketAddress='" + str(self.server.ip_address) + ":" + str(self.server.ws_port) + "';", 'utf-8')
                self.wfile.write(response)
            else:
                path = self.server.docpath + self.path
                if os.path.exists(path) and os.path.isdir(path):
                    index_files = ['/index.html', '/index.htm', ]
                    for index_file in index_files:
                        tmppath = path + index_file
                        if os.path.exists(tmppath):
                            path = tmppath
                            break

                _, ext = os.path.splitext(path)
                ext = ext.lower()
                content_type = {
                    '.css': 'text/css',
                    '.gif': 'image/gif',
                    '.htm': 'text/html',
                    '.html': 'text/html',
                    '.jpeg': 'image/jpeg',
                    '.jpg': 'image/jpg',
                    '.js': 'text/javascript',
                    '.png': 'image/png',
                    '.text': 'text/plain',
                    '.txt': 'text/plain',
                }

                if ext in content_type:
                    self.send_response(200)  # OK
                    self.send_header('Content-type', content_type[ext])
                    self.end_headers()

                    with open(path, 'rb') as ifp:
                        self.wfile.write(ifp.read())
                else:
                    self.send_response(200)  # OK
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()

                    with open(path, 'rb') as ifp:
                        self.wfile.write(ifp.read())

        except IOError:
            self.send_error(404, 'file not found')

    def relay_streaming(self, res):
        self.wfile.write("%s %d %s\r\n" % (self.protocol_version, res.status, res.reason))
        for line in res.headers.headers:
            self.wfile.write(line)
        self.end_headers()
        try:
            while not self.server.terminate:
                chunk = res.read(8192)
                if not chunk:
                    break
                self.wfile.write(chunk)
            self.wfile.flush()
        except socket.error:
            # connection closed by client
            pass

class _HTTPServer(ThreadingMixIn, HTTPServer):
    def __init__(self, address, web_port, ws_port, handler):
        HTTPServer.__init__(self, (address, web_port), handler)
        self.ip_address = address
        self.terminate = False
        self.ws_port = ws_port
        kervipath = os.path.dirname(kervi_ui.__file__)
        self.docpath = os.path.join(kervipath, "web/dist")

SERVER = None
ASSET_PATH = ""
def start(ip_address, http_port, ws_port):
    global SERVER
    SERVER = _HTTPServer(ip_address, http_port, ws_port, _HTTPRequestHandler)
    thread = threading.Thread(target=SERVER.serve_forever)
    thread.daemon = True
    thread.start()
    time.sleep(2)

def stop():
    print("stop web server")
    SERVER.terminate = True
    SERVER.shutdown()
