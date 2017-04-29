
#
# Copyright (C) 2000 Niall Smart.  All rights reserved
#

import re
import string

def findOSL(hay, needle, start = 0, end = None):
    "As string.find, except needle will not be found in a string literal"

    if start < 0:
        if (start < -len(hay)):
            start = -len(hay)
        add = len(hay) + start
    else:
        add = start

    if end == None:
        hay = hay[start:]
    else:
        hay = hay[start:end]

    start = 0
    nlen = len(needle)
    end = len(hay)

    while start < end:

        #
        # skip over string literals
        #

        if hay[start] in ['\'', '"']:
            if hay[start:start + 3] == '"""':
                tlen = 3
                tstr = '"""'
            else:
                tlen = 1
                tstr = hay[start]

            start = start + tlen

            while start < end:
                if hay[start:start + tlen] == tstr and hay[start - 1] != '\\':
                    start = start + tlen
                    break
                start = start + 1
            else:
                raise Exception("String literal not terminated")

            continue

        if hay[start:start + nlen] == needle:
            return start + add

        start = start + 1

    return -1


def extract(str, mark, schar, echar):

    end = 0
    tokens = []

    while 1:
        begin = string.find(str, mark, end)

        if begin == -1 or begin == len(str):
            if str[end:]:
                tokens.append(str[end:])
            break

        if str[begin + 1] != schar:
            #
            # [end:begin + 1] because x[n] == x[:n+1][-1]
            #
            tokens.append(str[end:begin + 1])
            end = begin + 1
            continue

        if begin > end:
            tokens.append(str[end:begin])

        end = findOSL(str, echar, begin + 2) + 1

        if end == 0:
            raise Exception("Terminating character ('%s') not found" % echar)

        tokens.append(str[begin:end])

    return tokens


def readBlock(inf, term):

    block = []

    while 1:
        line = inf.readline()
        if not line:
            raise Exception(
                "Unexpected end of file: %s terminator not found" % term)

        if re.match("^\s*%s" % term, line):
            return block

        block.append(line)

    return block

# vim: set et sts=4 sw=4 :
