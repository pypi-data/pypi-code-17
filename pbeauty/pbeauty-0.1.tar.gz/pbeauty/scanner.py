# -*- coding: utf-8 -*-

from errors import DecodeError

class IntScanner(object):
    ERROR = 'Expected integer for field default value.'
    def __init__(self, negetive = True):
        self.datas = []
        self.negetive = negetive

    def __call__(self, char):
        if char.isdigit() \
                or (self.negetive and not self.datas and char == '-'):
            self.datas.append(char)
            return 1
        return 0

    def value(self):
        return ''.join(self.datas)


class FloatScanner(object):
    ERROR = 'Expected number.'
    def __init__(self):
        self.datas = []
        return

    def __call__(self, char):
        if char == '-':
            if not self.datas:
                self.datas.append('-')
                return 1
            return 0

        if char.isdigit():
            self.datas.append(char)
            return 1

        if char == '.':
            if not char in self.datas:
                self.datas.append(char)
                return 1
            return 0
        return 0

    def value(self):
        return ''.join(self.datas)


class IdentifierScanner(object):
    ERROR = 'Expected Identifier.'
    def __init__(self):
        self.datas = []

    def __call__(self, char):
        if char.isalpha():
            self.datas.append(char)
            return 1

        if char == '_':
            self.datas.append(char)
            return 1

        if char.isdigit():
            if self.datas:
                self.datas.append(char)
                return 1
        return 0

    def value(self):
        return ''.join(self.datas)

class EnumScanner(IdentifierScanner):
    ERROR = 'Default value for an enum field must be an identifier.'
    def __init__(self, *args, **kwargs):
        IdentifierScanner.__init__(self, *args, **kwargs)
        return

class StringScanner(object):
    '''
    注意这个函数会把 '' 格式的字符串转换成 "" 格式的，为了与CPP等语言兼容.
    需要考虑转义字符.
    '''
    ERROR = "String literals cannot cross line boundaries."
    def __init__(self):
        self.datas = []
        self.escape_char = False
        self.end = False
        return

    def __call__(self, char):
        if self.end:
            return 0

        if char == '\n':
            return -1

        if not self.datas:
            if char not in ('\'', '"'):
                return 0
            self.datas.append(char)
            return 1

        self.datas.append(char)

        if self.escape_char:
            self.escape_char = False
            return 1

        if char == '\\':
            self.escape_char = True
            return 1

        if char == self.datas[0]:
            self.end = True
            return 1

        if char == '"':
            self.datas[-1] = '\\'
            self.datas.append(char)
            return 1
        return 1

    def value(self):
        if not self.datas:
            return ''
        self.datas[0] = '"'
        self.datas[-1] = '"'
        return ''.join(self.datas)

class BoolScanner(object):
    ERROR = 'Expected "true" or "false".'
    def __init__(self):
        self.string = None
        self.index = 0

    def __call__(self, char):
        if self.string is None:
            if char == 't':
                self.string = 'true'
            elif char == 'f':
                self.string = 'false'
            else:
                return 0
            return 1

        self.index += 1
        if self.index >= len(self.string):
            return 0
        return int(char == self.string[self.index])

    def value(self):
        return self.string


TYPE_TO_SCANNER = {}
def set_scanner(scanner, *keys):
    global TYPE_TO_SCANNER
    for key in keys:
        TYPE_TO_SCANNER[key] = scanner
    return
set_scanner(IntScanner,
            'int',
            'int32', 'uint32',
            'int64', 'uint64',
            'sint32', 'sint64',
            'fixed32', 'fixed64',
            'sfixed32', 'sfixed64',)

set_scanner(FloatScanner,
            'float', 'double',)

set_scanner(StringScanner,
            'string', 'bytes')

set_scanner(BoolScanner,
            'bool',)


class ScannerHelper(object):
    @staticmethod
    def TypeToScanner(type):
        return TYPE_TO_SCANNER.get(type, None)

class Context(object):
    def __init__(self, filename):
        self.filename = filename
        self.datas = open(filename, 'r').readlines()
        self.maxline = len(self.datas)
        self.lineno = 0
        self.cursor = 0
        self.comments = []

    def line(self):
        if self.lineno < self.maxline:
            return self.datas[self.lineno][self.cursor:]
        return ''

    def eof(self):
        return not self.line()

    def get_comments(self):
        comments = self.comments
        self.comments = []
        return comments

    def lstrip(self):
        skip = 0
        while self.lineno < self.maxline:
            line = self.datas[self.lineno]
            length = len(line)
            while self.cursor < length and line[self.cursor].isspace():
                self.cursor += 1
                skip += 1
            if self.cursor < length:
                break
            self.lineno += 1
            self.cursor = 0
        return skip

    def skip_comments(self):
        while self.lineno < self.maxline:
            self.lstrip()
            line = self.line()
            if line.startswith('//'):
                self.lineno += 1
                self.cursor = 0
                comment = line[2:].strip()
                if comment:
                    self.comments.append(comment)
                continue
            break

    def skip_semicolon(self):
        total = 0
        while True:
            self.skip_comments()
            count = 0
            while self.findstring(';', alert = False):
                count += 1
                continue
            total += count
            if count == 0:
                return total
        return total

    def findstring(self, string, alert = False):
        self.skip_comments()
        if self.line().startswith(string):
            self.cursor += len(string)
            return True
        if alert:
            raise self.error('Expected "%s".' % string)
        return False

    def findspace(self):
        line = self.line()
        if not line:
            return False
        if line[0].isspace():
            self.cursor += 1
            return True
        return False

    def findraw(self, scanner = None):
        self.skip_comments()
        line = self.line()
        if not line:
            return
        length = len(line)
        cursor = 0
        if scanner is None:
            scanner = IdentifierScanner()
        while cursor < length:
            result = scanner(line[cursor])
            if result < 0:
                raise self.error(scanner.ERROR)
            if result == 0:
                break
            cursor += 1
        if cursor > 0:
            identifier = line[:cursor]
            self.cursor += cursor
            return identifier
        return

    def error(self, string):
        return DecodeError(self, string)


