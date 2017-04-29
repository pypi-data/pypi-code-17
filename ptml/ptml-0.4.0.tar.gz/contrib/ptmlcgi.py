#!/usr/local/bin/python

#
# Copyright (C) 2000 Niall Smart.  All rights reserved.
#

#
# Note: This file prints out the full details of any exception to
#       stdout, this may include the details of your directory
#       structure and possibly other information you want to keep
#       private.
#

import sys
import os
import cgi
import traceback
import string
import cStringIO

from string import *
from ptml.AutoParser import AutoParser
from ptml.PTMLResponse import PTMLResponse
from ptml.CGIRequest import CGIRequest

oldstdout = None
exitcode = 0

try:
    ap = AutoParser(
        "/usr/local/web/ptml/htdocs",
        "/usr/local/web/ptml/cache",
        AutoParser.CRC
    )

    if not os.environ.has_key("PATH_INFO"):
        raise Exception("No PATH_INFO environment variable")
        sys.exit(0)

    cache = ap.handleRequest(os.environ["PATH_INFO"])

    resp = PTMLResponse()
    req = CGIRequest()
    buf = cStringIO.StringIO()

    oldstdout = sys.stdout
    sys.stdout = buf

    try:
        execfile(cache, {"stdout": buf, "response": resp, "request": req})
    except SystemExit, code:
        exitcode = code

    sys.stdout = oldstdout
    headers = resp.getHeaders()

    status = 0
    content_type = 0

    for k in headers.keys():
        sys.stdout.write("%s: %s\n" % (k, headers[k]))

        if string.lower(k) == "status":
            status = 1

        if string.lower(k) == "content-type":
            content_type = 1

    if status == 0:
        sys.stdout.write("Status: 200\n")

    if content_type == 0:
        sys.stdout.write("Content-type: text/html\n")

    sys.stdout.write("\n")
    sys.stdout.write(buf.getvalue())


except:
    lines = apply(traceback.format_exception, sys.exc_info())

    if oldstdout != None:
        sys.stdout = oldstdout

    print "Status: 500"
    print "Content-type: text/html"
    print ""
    print "<html><head><title>Fatal Exception</title></head><body>"
    print "<h1>Fatal Exception</h1><pre>"
    print cgi.escape(join(lines))
    print "</pre></body></html>"

sys.exit(exitcode)

# vim: set et sts=4 sw=4 :
