
#
# Copyright (C) 2000 Niall Smart.  All rights reserved.
#

import codecs
import itertools
import re
import sys
from string import *

if __name__ == "__main__":
    import os.path
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    parent = os.path.normpath(path + "/../")
    sys.path.append(parent)

from ptml.util import *

class TemplateParser:

    def __init__(this, _inf, _outf):
        this.inf = _inf
        this.outf = _outf
        this.tab = 0
        this.dedent = [[]]
        this.indent = []
        this.coding = None
        this.str_code = "str(%s)"
        this.lineno = 0


    def set_coding(this, coding):
        codec_info = codecs.lookup(coding)
        if this.coding and (this.coding != codec_info.name):
            raise Exception("Cannot change output encoding from '%s' to '%s'"
                " in line %i" % (this.coding, codec_info.name, this.lineno))
        this.coding = codec_info.name
        this.str_code = "unicode(%%s).encode(%r)" % this.coding


    def debug(this, str, *args):
        this.writeln("#")
        this.writeln("# " + str % args)
        this.writeln("#")


    def writeln(this, line, tab = None):
        if tab is None:
            tab = this.tab
        this.outf.write("%s%s\n" % ("\t" * tab, line))


    def echo(this, line):
        if "\\" in line:
            line = replace(line, "\\", "\\\\")

        if "\t" in line:
            line = replace(line, "\t", "\\t")

        if "'" in line:
            line = replace(line, "'", "\\\'")

        if line[-1] == "\n":
            line = replace(line, "\n", "\\n")

        this.writeln("stdout.write('%s')" % line)


    def exprEchoToStmt(this, line):
        parts = []
        for part in extract(line, "$", "{", "}"):
            if part[0:2] == "${":
                if len(part) == 3:
                    raise Exception(
                        "Empty expression echo directive (${}) is not allowed"
                        " in line %i" % this.lineno)
                part = "%%{ stdout.write(%s) }" % (this.str_code % part[2:-1])

            parts.append(part)


        return join(parts, "")


    def backtab(this):
        """Decrease indentation level"""
        if this.tab == 0:
            raise Exception("Cannot have negative indentation level"
                " in line %i" % this.lineno)
        this.tab = this.tab - 1
        del this.indent[-1], this.dedent[-1]


    def handleStmtLine(this, line):

        for token in extract(line, "%", "{", "}"):

            if token[0:2] != "%{":
                this.echo(token)
                continue

            stmt = strip(token[2:-1])

            if stmt == "":
                this.backtab()
                continue

            if stmt.startswith("#end"):
                dedent = stmt[4:]
                while this.indent:
                    indent = this.indent[-1]
                    this.backtab()
                    if indent.startswith(dedent):
                        break
                else:
                    raise Exception("No match found for %s in line %i"
                        % (stmt, this.lineno))
                continue

            if stmt[-1] != ":":
                this.writeln(stmt)
                continue

            [word, rest] = split(stmt + " x", None, 1)

            this.debug("word=%s, dedent=%s", word, this.dedent[-1])

            if word in this.dedent[-1]:
                this.writeln(stmt, tab = this.tab - 1)
            else:
                this.writeln(stmt)

                this.tab = this.tab + 1
                this.indent.append(stmt)

                if word == "if":
                    this.dedent.append(["elif", "else:"])
                elif word == "for":
                    this.dedent.append(["else:"])
                elif word == "try:":
                    this.dedent.append(["except", "except:", "finally:"])
                elif word == "while":
                    this.dedent.append(["else:"])
                elif word in ("def", "class"):
                    this.dedent.append([])

    def handleTextBlock(this, block):

        for line in block:
            this.echo(line + "\n")


    def handlePythonBlock(this, block):

        if len(block) == 0:
            return

        block = map(expandtabs, block)

        first = -1

        for line in block:

            indent = len(line) - len(lstrip(line))

            if first == -1:
                if lstrip(line) != "":
                    first = indent
            elif indent < first and len(lstrip(line)) > 0:
                raise Exception(
                    "Cannot decrease indentation level in Python block"
                    " in line %i" % this.lineno)

            this.writeln(line[first:-1])


    def check_coding(this, line):
        """Raise ValueError if line does not match coding"""
        if this.coding:
            try:
                line.decode(this.coding)
            except UnicodeError, _err:
                raise ValueError("Line %i contains invalid char: %s" % (
                    this.lineno, _err))


    def parse(this):

        for this.lineno in itertools.count(1):

            line = this.inf.readline()
            if not line:
                break

            this.check_coding(line)

            if (this.lineno == 1) and line.startswith(codecs.BOM_UTF8):
                this.set_coding("utf-8")
                this.writeln(codecs.BOM_UTF8)
                this.writeln("import codecs")
                this.writeln("stdout.write(codecs.BOM_UTF8)")
                line = line[len(codecs.BOM_UTF8):]

            if re.match(r"^\s*<%python>\s*$", line):
                this.handlePythonBlock(readBlock(this.inf, "</%python>"))
                continue
            elif re.match(r"^\s*<%text>\s*$", line):
                this.handleTextBlock(readBlock(this.inf, "</%text>"))
                continue

            if "$" in line:
                line = this.exprEchoToStmt(line)

            if "%" in line:
                m = re.match(r"^\s*%([^{]|$)", line)

                if this.lineno <= 2:
                    c_m = re.search(r"#.*coding[=:]\s*([-\w.]+).*", line)
                    if c_m:
                        this.set_coding(c_m.group(1))

                if m != None:
                    line = replace(line, "%", "%{ ", 1) + " }"

                this.handleStmtLine(line)
            else:
                this.echo(line)

        if this.tab != 0:
            raise Exception("Unexpected end of file: missing block closure")



if __name__ == "__main__":
    print "from sys import stdout"
    p = TemplateParser(sys.stdin, sys.stdout)
    p.parse()

# vim: set et sts=4 sw=4 :
