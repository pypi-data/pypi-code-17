#!/usr/local/bin/python

import os
import sys
import traceback

from glob import glob
from StringIO import StringIO
from string import join
from sys import argv
from ptml.TemplateParser import TemplateParser
from os.path import isfile


def formatException(exTuple):
    (type, message, tb) = exTuple
    return "%s: %s" % (type.__name__, message)


def runComparisonTest(inf, outf, tmpf):

    tmpf = StringIO()
    generateTestFile(inf, tmpf)

    return outf.read() == tmpf.getvalue()


def generateTestFile(inf, outf):

    ex = None
    parsef = StringIO()

    try:
        tp = TemplateParser(inf, parsef)
        tp.parse()
    except:
        outf.write("\nPARSE EXCEPTION\n")
        outf.write("%s\n" % formatException(sys.exc_info()))
        return

    svstdout, svstderr = sys.stdout, sys.stderr

    stdout = sys.stdout = StringIO()
    stderr = sys.stderr = StringIO()

    try:
        exec(parsef.getvalue())
    except Exception:
        ex = formatException(sys.exc_info())

    sys.stdout, sys.stderr = svstdout, svstderr

    outf.write("STDOUT\n")
    outf.write(stdout.getvalue())
    outf.write("\nSTDERR\n")
    outf.write(stderr.getvalue())

    if ex != None:
        outf.write("\nEXECUTION EXCEPTION\n")
        outf.write("%s\n" % ex)


if not (len(argv) == 1 or (len(argv) == 2 and argv[1] == "-r")):
    sys.stderr.write("usage: %s [-g]\n" % argv[0])
    sys.exit(1)


failed = []

for ifilename in glob("*.ptml"):

    testname = ifilename[0:-5]
    ofilename = testname + ".dat"
    efilename = testname + ".err"

    if len(argv) == 1:
        strf = StringIO()
        outf = open(ofilename)

        generateTestFile(open(ifilename), strf)

        if strf.getvalue() == outf.read():
            print "%s: ok" % testname
            if os.access(efilename, os.F_OK):
                os.remove(efilename)
        else:
            print "%s: fail" % testname
            failed.append(testname)
            errf = open(efilename, "w")
            errf.write(strf.getvalue())
            errf.close()

    else:
        sys.stderr.write("generating %s from %s\n" % (ofilename, ifilename))
        generateTestFile(open(ifilename), open(ofilename, "w"))


if len(failed) > 0:
    sys.stdout = sys.stderr
    print
    print "WARNING: the following tests failed: "
    print
    print join(failed, ", ")
    print

# vim: set et sts=4 sw=4 :
