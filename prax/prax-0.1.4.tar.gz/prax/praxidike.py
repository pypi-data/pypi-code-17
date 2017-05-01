#!/usr/bin/env python
from __future__ import absolute_import, division, print_function
from future.builtins import (str, super, int, object)

import argparse
import base64
import binascii
import functools
import math
import string
import os
import sys
from grako.exceptions import FailedParse

from prax import parser


def compose(*functions):
    """Combines one or more functions into a single function"""
    if len(functions) == 0:
        return None
    elif len(functions) == 1:
        return functions[0]
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


class Formatter(object):
    """A standard formatting object

       Used to simplify parsing of literals by condensing repetitive formatting rules into
       single classes"""
    def __init__(self, check=lambda x: True, strip=lambda x: x, add=lambda x: x):
        self.check = check
        self.strip = strip
        self.add = add


class StartsWith(Formatter):
    """Formatter for types that start with a specific string"""
    def __init__(self, starts_with):
        self.starts_with = starts_with
        super().__init__(check=lambda x: x.startswith(self.starts_with),
                         strip=lambda x: x[len(self.starts_with):],
                         add=lambda x: self.starts_with + x)


class EvenNum(Formatter):
    """Formatter for types that require an even length (hex)"""
    def __init__(self, padding_char):
        self.padding_char = padding_char
        super().__init__(check=lambda x: len(x) % 2 == 0,
                         strip=lambda x: x,
                         add=lambda x: x if self.check(x) else self.padding_char + x)


class EndsWith(Formatter):
    """Formatter for types that end with a specific string"""
    def __init__(self, ends_with):
        self.ends_with = ends_with
        super().__init__(check=lambda x: x.endswith(self.ends_with),
                         strip=lambda x: x[:len(self.ends_with)],
                         add=lambda x: x + self.ends_with)

class Thing(object):
    NAME = None
    FLAG = None


class Operator(Thing):
    """Base class for operators

    subclasses must implement NAME, FLAG, and operate"""

    @classmethod
    def add_args(cls, parser):
        """Adds argument to an ArgumentParser according to NAME and FLAG"""
        parser.add_argument("-{}".format(cls.FLAG), action='store_true', default=False,
                            help='Apply "{}" operator to data'.format(cls.NAME))
        return parser

    @staticmethod
    def operate(self, number):
        """performs an operation on value"""
        return number


class SwapEndianness(Operator):
    """Swaps the endianness of a value

    Currently swaps the byte order of the full string
    should consider options to allow for selecting a byte length to swap inside the value"""
    NAME = 'swap endianness'
    FLAG = 'e'

    @classmethod
    def operate(self, number):
        """Swaps the endianness of a value

        int.to_bytes requires a length of bytes so we take ceil(log(number)/(2*log(16)))
        to make sure nothing is truncated"""
        log = math.log(number, 16)
        ceil = math.ceil(log / 2)
        bytes_ = number.to_bytes(ceil, 'big')
        return int.from_bytes(bytes_, 'little')


class Type(Thing):
    """Base class for input/output types

    subclasses Must define NAME, FLAG, _to_int, _to_str"""
    FORMATTERS = []

    @classmethod
    def add_args(cls, parser):
        """adds arguments according to NAME and FLAG"""
        parser.add_argument("-{}".format(cls.FLAG.lower()), action='store_true', default=False,
                            help="output in {}".format(cls.NAME))
        parser.add_argument("-{}".format(cls.FLAG.upper()), action='store_true', default=False,
                            help="force input as {}".format(cls.NAME))
        return parser

    @classmethod
    def strip_format(cls, string_):
        """Strips formatting of this type from a string

        return None if formatting is not present"""
        return string_

    @classmethod
    def add_format(cls, string_):
        """Adds formatting of this type to a string"""
        return string_

    @classmethod
    def convert(cls, number):
        """Converts an int to a formatted string of this type"""
        return cls.add_format(cls._to_str(number))

    @classmethod
    def parse(cls, string_):
        """converts a formatted string of this type to an int"""
        return cls._to_int(cls.strip_format(string_))

    @classmethod
    def _to_int(cls, string_):
        """Converts an unformatted string of this type to an int

        Must be implemented by subclass"""
        raise NotImplementedError

    @classmethod
    def _to_str(cls, number):
        """Converts an int to an unformatted string of this type

        Must be implemented by subclass"""
        raise NotImplementedError


class Base(Type):
    """Base class for generic base conversions (not base64)

    subclass must specify BASE=int and optionally FORMATTERS"""
    BASE = None
    ALPHABET = string.digits + string.ascii_lowercase

    @classmethod
    def strip_format(cls, string_):
        for fmt in cls.FORMATTERS:
            if fmt.check(string_):
                string_ = fmt.strip(string_)
            else:
                return None
        return string_

    @classmethod
    def add_format(cls, string_):
        for fmt in reversed(cls.FORMATTERS):
            string_ = fmt.add(string_)
        return string_

    @classmethod
    def parse(cls, string_, force=False):
        stripped = cls.strip_format(string_)
        if stripped is not None:  # string_ fits formatting of this type
            return cls._to_int(stripped)
        if force:
            return cls._to_int(string_)
        return None

    @classmethod
    def convert(cls, *args):
        val = "".join([cls._to_str(x) for x in args])
        return cls.add_format(val)

    @classmethod
    def _to_int(cls, string_):
        try:
            return int(string_, cls.BASE)
        except ValueError:
            return None

    # http://interactivepython.org/courselib/static/pythonds/Recursion/pythondsConvertinganIntegertoastring_inAnyBase.html
    @classmethod
    def _to_str(cls, number):
        if cls.BASE > len(cls.ALPHABET):
            raise ArithmeticError("Too large of a base for alphabet")
        if number < cls.BASE:
            return cls.ALPHABET[number]
        else:
            return cls._to_str(number // cls.BASE) + cls.ALPHABET[number % cls.BASE]


class BaseHex(Base):
    NAME = 'hex'
    BASE = 16
    FLAG = 'x'
    FORMATTERS = [StartsWith('0x'), EvenNum('0')]


class BaseDecimal(Base):
    NAME = 'decimal'
    BASE = 10
    FLAG = 'd'


class BaseOctal(Base):
    NAME = 'octal'
    BASE = 8
    FLAG = 'o'
    FORMATTERS = [StartsWith('0o')]


class BaseBinary(Base):
    NAME = 'binary'
    BASE = 2
    FLAG = 'b'
    FORMATTERS = [StartsWith('0b')]


class Ascii(Type):
    NAME = 'ascii'
    FLAG = 'r'

    @classmethod
    def _to_str(cls, *number):
        # convert int -> even numbered hex -> bytes -> raw
        i = "".join([EvenNum('0').add(BaseHex._to_str(x)) for x in number])
        return binascii.unhexlify(i).decode('latin-1')

    @classmethod
    def _to_int(cls, string_):
        if string_ is None:
            return None
        if type(string_) is str:
            string_ = string_.encode('latin-1')
        return BaseHex.parse(binascii.hexlify(string_).decode('latin1'), force=True)


class Base64(Ascii):
    """Base64 type

    Inherits from ascii because all internal operations should be performed on strings
    so that b64 conversion doesn't pad in the middle of the string"""
    NAME = "Base64"
    FLAG = 's'

    @classmethod
    def strip_format(cls, string_):
        try:
            return base64.b64decode(string_)
        except (binascii.Error, TypeError):
            return None

    @classmethod
    def add_format(cls, string_):
        try:
            return base64.b64encode(string_.encode('latin-1')).decode('latin-1')
        except:
            return None


types = [BaseHex, BaseDecimal, Ascii, Base64]
target_types = types + [BaseBinary, BaseOctal]
operators = [SwapEndianness]


def parse_to_int(string_):
    """Helper function to get the value of the first type"""
    return [y for y in [x.parse(string_) for x in types] if y is not None][0]

def raw_print(string_, end="\n"):
    sys.stdout.buffer.write(string_.encode("latin-1"))
    sys.stdout.buffer.write(end.encode("latin-1"))
    sys.stdout.flush()

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("input", nargs='+', help="literal or expression to parse")
    arg_parser.add_argument("-n", action='store_true', help="don't print newline")
    for x in target_types + operators:
        arg_parser = x.add_args(arg_parser)
    args = arg_parser.parse_args()
    print_end = "" if args.n else os.linesep
    args_dict = vars(args)

    input_type = None
    output_type = None
    for x in target_types:
        if args_dict[x.FLAG.lower()]:
            output_type = x
        if args_dict[x.FLAG.upper()]:
            input_type = x

    funcs = [x.operate for x in operators if args_dict[x.FLAG]]
    ops = compose(*funcs)

    # avoids a circular import
    from prax import semantics

    argument = " ".join(args.input)
    if output_type is None:
        values = []
        for x in types:
            p = parser.PraxParser(semantics=semantics.PraxSemantics(x, input_type, operators=ops))
            try:
                values.append(x.add_format(p.parse(argument)))
            except FailedParse:
                print("Invalid syntax")
                exit(1)
        raw_print(" ".join(values), "\n")
    else:
        p = parser.PraxParser(semantics=semantics.PraxSemantics(output_type, input_type, operators=ops))
        raw_print(output_type.add_format(p.parse(argument)), end=print_end)


if __name__ == "__main__":
    main()
