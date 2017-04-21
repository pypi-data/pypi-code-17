#!/usr/bin/python

import re
from patterns import *

class PatternCompiler(object):
    VALID_PATTERN_RE = re.compile(r'(^\$(\d+)?\{(\w+)(?:\((.+)\))?([\*\+\?|!])?\}?$)')
    REGEX_SPECIALS_RE = re.compile(r'([\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|])', re.MULTILINE | re.DOTALL)
    CAPTURE_INDEX_RE = re.compile(r'(\$\d+)')
    SPACIAL_RE = re.compile(r'\$|\{|\}|\(|\)')

    def __init__(self, pattern_set=None):
        self.__pattern_set = DEFAULT_PATTERN_SET
        if pattern_set:
            self.register(pattern_set)

    def register(self, pattern_set=dict()):
        self.__pattern_set.update(pattern_set)

    def compile(self, pattern, capture_names=list()):
        exprs = self.__split(pattern)
        compiled = self.__escape(pattern)
        compiled = re.sub(r'(^\s+)|(\s+$)', '', compiled)
        compiled = re.sub(r'\s+', '\s+', compiled)
        for expr in exprs:
            p = self.__compile_expr(expr, capture_names)
            if p:
                compiled = compiled.replace(self.__escape(expr), p)

        return r'(?:%s)' % compiled

    def __check_special(self, special, s):
        if special:
            if self.SPACIAL_RE.match(special):
                s += special

        special = ''
        return (special, s)

    def __split(self, pattern):
        s = ''
        special = ''
        esc = False
        in_expr = False
        in_group = False
        exps = []

        i = 0
        while i < len(pattern):
            c = pattern[i]
            i += 1

            if c == '$':
                special, s = self.__check_special(special, s)
                if not esc and not in_expr:
                    special = c
                    s = ''
                    continue
            elif c == '{':
                if not esc and not in_expr and (special == '$' or re.match(self.CAPTURE_INDEX_RE, s)):
                    in_expr = True
                    special, s = self.__check_special(special, s)
                    special = c
                    continue
            elif c == '}':
                if not esc and in_expr and not in_group:
                    special, s = self.__check_special(special, s)
                    s += c
                    exps.append(s)
                    s = ''
                    in_expr = False
                    continue
            elif c == '(':
                if in_expr and not in_group and not esc:
                    special, s = self.__check_special(special, s)
                    special = c
                    in_group = True
                    continue
            elif c == ')':
                if in_group and not esc:
                    in_group = False
            elif c == '\n' or c == '\r':
                continue

            special, s = self.__check_special(special, s)
            esc = False
            s += c

        return exps

    def __escape(self, input):
        return self.REGEX_SPECIALS_RE.sub(r'\\\1', input)

    def __compile_expr(self, expr, capture_names=list()):
        match = self.VALID_PATTERN_RE.match(expr)
        if not match:
            return None

        g = match.groups()
        gi = int(g[1]) if g[1] else None
        key = g[2]

        gn = capture_names[gi - 1] if gi else None
        suffix = g[4] or ''
        is_negative = suffix == '!'
        result = self.__pattern_set[key]
        if callable(result):
            if g[3]:
                result = result(self.__escape(g[3]) if result.escepable() \
                                else g[3], capture_name=gn, is_negative=is_negative)
            else:
                result = result(capture_name=gn)

        elif is_negative:
            result = '(?!%s)' % result

        if gn:
            return "(?P<%s>(%s)%s)" % (gn, result, g[4] or '')

        if g[4]:
            return '(%s)%s' % (result, g[4] or '')

        return result
