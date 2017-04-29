#!/usr/local/bin/python

import socket
import sys
import os

from ptml.AutoParser import AutoParser
from ptml.PTMLHTTPServer import PTMLHTTPServer
from ptml.PTMLHTTPServer import PTMLHTTPRequestHandler


if len(sys.argv) != 5:
    sys.stderr.write(
        "usage: %s [always|mtime|crc] [py|pyc|pyo] <port> <hits>\n"
        % sys.argv[0])
    sys.exit(1)

if sys.argv[1] == "always":
    mode = AutoParser.ALWAYS
elif sys.argv[1] == "mtime":
    mode = AutoParser.MTIME
elif sys.argv[1] == "crc":
    mode = AutoParser.CRC

port = int(sys.argv[3])
hits = int(sys.argv[4])

ap = AutoParser(os.getcwd() + "/htdocs", os.getcwd() + "/cache", mode)

httpd = PTMLHTTPServer(('127.0.0.1', port), ap, PTMLHTTPRequestHandler)

httpd.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sys.stderr.write("httpd: listening on 127.0.0.1:%s\n" % port)

for i in range(0, hits):
    httpd.handle_request()

sys.stderr.write("httpd: serviced %s requests; exiting\n" % hits)

# vim: set et sts=4 sw=4 :
