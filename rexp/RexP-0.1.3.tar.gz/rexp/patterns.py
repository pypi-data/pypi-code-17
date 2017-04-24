#!/usr/bin/python

import re


class Pattern(object):
    def escepable(self):
        return True

    def __call__(self, *args, **kwargs):
        return '' if not len(args) else re.escape(args[0])


class RegexPattern(Pattern):
    def escepable(self):
        return False

    def __call__(self, *args, **kwargs):
        if not len(args):
            raise ValueError('Invalid expression!')

        return args[0]


class RegexGroupPattern(Pattern):
    def __call__(self, *args, **kwargs):
        # TODO: validate.
        is_negative = kwargs['is_negative'] or False
        return '[%s%s]' % ('^' if is_negative else '', args[0])


class RegexNotPattern(Pattern):
    def escepable(self):
        return False

    def __call__(self, *args, **kwargs):
        return '(?!%s)' % args[0]


class KeyValuePairPattern(Pattern):
    def escepable(self):
        return False

    def __call__(self, *args, **kwargs):
        sep = r'=' if not len(args) else args[0]
        sep_esced = re.escape(sep)

        post_check = r'[\,\;\b]' if len(args) < 2 else args[1]
        post_check_esced = re.escape(post_check)

        cn = kwargs['capture_name']
        return r'\b(?P<{2}key>[^{0}\s]+)\s*{0}\s*(?P<{2}value>[^{0}]+)(({1})|$)'.format(
            sep if sep == sep_esced else sep_esced,
            post_check if post_check == post_check_esced else post_check_esced,
            '%s_' % cn if cn else '', )


class DateTimePattern(Pattern):
    WILDCARD_RE = re.compile(r'%(?P<c>((?!%)[a-zA-Z])|%)', re.IGNORECASE)

    def __init__(self):
        self.__wildcards = [
            ('d', r'(([0-2][0-9])|(3[0-1]))'),
            ('f', r'\d{3,6}'),
            ('H', r'(([0-1][0-9])|(2[0-3]))'),
            ('I', r'((0[0-9])|(1[0-2]))'),
            ('m', r'((0[0-9])|(1[0-2]))'),
            ('M', r'([0-5][0-9])'),
            ('p', r'((AM)|(PM))'),
            ('S', r'(([0-5][0-9])|(6[0-1]))'),
            ('Y', r'((?:19|20)[0-9]{2})'),
            ('y', r'([0-9]{2})'),
            ('z', r'((-|\+)(([0-1][0-9])|(2[0-3])):([0-5][0-9]))'),
            ('%', r'(%)')
        ]

    def __call__(self, *args, **kwargs):
        if not len(args):
            raise ValueError('Invalid format')

        f = str(args[0])
        l = []
        for x in self.WILDCARD_RE.finditer(f):
            c = x.group('c')
            w = [x for x in self.__wildcards if x[0] == c]
            if len(w):
                l.append(w[0])

        for x in l:
            f = f.replace('%{0}'.format(x[0]), x[1])

        return f


class IPAddressPattern(Pattern):
    __V4_EXPR = r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})'
    __V6_EXPR = r'((([0-9A-Fa-f]{1,4}:){1,6}:)|(([0-9A-Fa-f]{1,4}:){7}))([0-9A-Fa-f]{1,4})'

    def __call__(self, *args, **kwargs):
        if not len(args) or not re.match(r'^(v4)|(v6)$', args[0]):
            return r'(%s|%s)' % (self.__V4_EXPR, self.__V6_EXPR)

        return self.__V6_EXPR if str(args[0]).lower() == 'v6' \
            else self.__V4_EXPR


class PathPattern(Pattern):
    def __call__(self, *args, **kwargs):
        sep = '/'
        if len(args) > 0:
            sep = str(args[0]).strip()

        if not re.match(r'(\/|\\)', sep):
            raise ValueError('Invalid path seperator!')

        return r'({0}(\{1}[^\{1}]+)+(\{1}$)?)' \
            .format('([a-zA-Z]+:)' if sep == '\\' else '', sep)


class UUIDPattern(Pattern):
    def __init__(self):
        self.__format = r'[0-9a-f]{8}-[0-9a-f]{4}-%s[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}'

    def __call__(self, *args, **kwargs):
        if len(args):
            ver = int(args[0])
            if ver > 0 and ver < 6:
                return self.__format % ver

            raise ValueError('Invalid uuid version!')

        return self.__format % '[1-5]'


DEFAULT_PATTERN_SET = dict(
    RE=RegexPattern(),
    BEGIN=r'^',
    END=r'$',
    GR=RegexGroupPattern(),
    NOT=RegexNotPattern(),
    SPACE=r'\s',
    ANY=r'.',
    INT=r'\d+',
    NUM=r'(\d+([,\.]\d+)*)',
    CH="\w",
    STR=r'("["]+")|(\'[\'+]\')',
    WORD=r'\b\w+\b',
    WORDS=r'\b(\w+\s*)*\b',
    PATH=PathPattern(),
    URL=r'https?:\/\/(([^\/]+)(\/[^\/|?]*))(\?[^&]+(&[^&]+)*)',
    RELATIVE_URL=r'((\/[^\/|?]+)+)(\?[^&]+(&[^&]+)*)',
    DATE=DateTimePattern(),
    IP=IPAddressPattern(),
    IP4='${IP(v4)}',
    IP6='${IP(v6)}',
    IPV4='${IP(v4)}',
    IPV6='${IP(v6)}',
    UUID=UUIDPattern(),
    UUID1='${UUID(1)}',
    UUID2='${UUID(2)}',
    UUID3='${UUID(3)}',
    UUID4='${UUID(4)}',
    UUID5='${UUID(5)}',
    PAIR=KeyValuePairPattern()
)
