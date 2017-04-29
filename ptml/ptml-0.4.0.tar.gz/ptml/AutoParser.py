
#
# Copyright (C) 2000 Niall Smart.  All rights reserved.
#

import sys
import re
import zlib

import os
import stat
import cStringIO

from os.path import isabs, isdir, isfile, dirname, normpath
from string import *

from ptml.TemplateParser import TemplateParser
from ptml.PTMLResponse import PTMLResponse

from ptml.Exceptions import *

class AutoParser:

    ALWAYS = 0
    MTIME = 1
    CRC = 2

    accept_regex = r"^[a-zA-Z0-9_./\-]+$"

    def __init__(this, _root, _cache, _compare = MTIME):
        this.root = _root
        this.cache = _cache
        this.compare = _compare

        if not isabs(this.root):
            raise Exception(
                "Root directory must be specified as absolute path")
        elif not isdir(this.root):
            raise Exception("Root directory not found: %s" % this.root)

        if not isabs(this.cache):
            raise Exception(
                "Cache directory must be specified as absolute path")
        elif not isdir(this.cache):
            raise Exception("Cache directory not found: %s" % this.cache)


    def debug(this, str, *args):
        #sys.stderr.write(str % args + "\n")
        pass


    def calcCRC(this, f):
        return reduce(lambda x, y: zlib.adler32(y, x), f.readlines(), 0)


    def compareCRC(this, source, cache):

        scrc = this.calcCRC(open(source))

        try:
            ccrcf = open(cache + ".crc", "r")
        except:
            this.debug("CRC file not found: file=%s" % cache + ".crc")
            return 1

        ccrc = ccrcf.readline()[:-1]

        return str(ccrc) != str(scrc)


    def compareModificationTime(this, source, cache):

        sstat = os.stat(source)

        try:
            cstat = os.stat(cache)
        except:
            return 1

        return sstat[stat.ST_MTIME] > cstat[stat.ST_MTIME]


    def parseIsNecessary(this, source, cache):

        if this.compare == AutoParser.ALWAYS:


            return 1
        elif this.compare == AutoParser.MTIME:
            return this.compareModificationTime(source, cache)
        elif this.compare == AutoParser.CRC:
            return this.compareCRC(source, cache)
        else:
            raise Exception("Invalid comparison method: %s" % this.compare)


    def parseIfNecessary(this, source, cache):

        if not this.parseIsNecessary(source, cache):
            return

        this.debug("parse is necessary: source=%s" % source)

        sourcef = open(source)

        if not isdir(dirname(cache)):
            os.makedirs(dirname(cache))

        cachef = open(cache, "w")
        parser = TemplateParser(sourcef, cachef)
        parser.parse()

        if this.compare == AutoParser.CRC:
            sourcef.seek(0)
            crcf = open(cache + ".crc", "w")
            crcf.write(str(this.calcCRC(sourcef)) + "\n")



    def handleRequest(this, path):

        if find(path, "..") >= 0:
            raise Exception("Relative paths not allowed")

        if not re.match(this.accept_regex, path):
            raise FileNotFoundException("Invalid path")

        source = normpath(this.root + "/" + path)
        cache = normpath(this.cache + "/" + path + ".py")

        this.debug("new request: source=%s cache=%s" % (source, cache))

        if not isfile(source):
            raise FileNotFoundException()

        this.parseIfNecessary(source, cache)

        return cache

# vim: set et sts=4 sw=4 :
