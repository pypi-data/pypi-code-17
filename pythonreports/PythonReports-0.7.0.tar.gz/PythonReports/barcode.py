"""BarCode routines"""
"""History:
25-nov-2007 [als]   fix default value for errors parameter to __call__
05-dec-2006 [als]   sweep pylint warnings
07-nov-2006 [als]   fix doctests (no quet zones encoded)
22-sep-2006 [als]   encoding calls return sequences w/o quiet zones;
                    added .add_qz(), .min_height()
12-sep-2006 [als]   created
"""
__version__ = "$Revision: 1.4 $"[11:-2]
__date__ = "$Date: 2007/11/25 08:48:41 $"[7:-2]

__all__ = ["code2of5i", "code39", "code128"]

import itertools
import math
import re

_re_digit = re.compile("\d")
_re_nondigit = re.compile("\D")

class InvalidLiteral(ValueError):

    """Error raised when a character cannot be encoded"""

    def __init__(self, text, barcode):
        ValueError.__init__(self, text, barcode)
        self.text = text
        self.barcode = barcode

    def __str__(self):
        return "Invalid text for %s: %r" % (
            self.barcode.__class__.__name__, self.text)

class BarCode(object):

    """Base class for BarCode encoders

    BarCode objects are stateless callables,
    meant to be used as singletons.

    """

    # minimum size of quiet zones, in mils
    # 2of5I and Code128 require .25inch, Code39 require .10inch
    QZ_MILS = 250

    def __call__(self, text, errors="strict"):
        """Encode passed text, return sequence of stripe widths

        Parameters:
            text: string to encode
            errors: error handling scheme: "strict" or "ignore".

        Return value: tuple of numeric values for space an bar
        widths.  Each value is a multiplier for X dimension.
        The first and the last values are widths of the outermost
        bars.  The caller must ensure that there are wide enough
        quiet zones on both sides of the symbol.

        """

    def add_qz(self, sequence, xdim):
        """Return barcode sequence with added quiet zones

        Parameters:
            sequence: a sequence of bar/space widths relative
                to X dimension, as returned by the encoder.
            xdim: X dimension in mils (a mil is 1/1000 inch).

        Return value: sequence with added widths of quiet zones
        on both sides of the symbol.

        Note: the minimum X-dimension for an "open system"
        (a bar code label that will be read by scanners from
        outside your company) is 7.5 mils.

        """
        # the width of quiet zones is 10X or self.QZ_MILS,
        # whichever is greater
        _qz = int(math.ceil(float(max(xdim * 10, self.QZ_MILS)) / xdim))
        return (_qz,) + tuple(sequence) + (_qz,)

    def min_height(self, sequence, xdim):
        """Return minimum height of the symbol in points

        Parameters:
            sequence: a sequence of bar/space widths relative
                to X dimension, as returned by the encoder.
            xdim: X dimension in mils (a mil is 1/1000 inch).

        Return value: required symbol height as an integer
        number of points (a point is 1/72 inch).

        Note: the minimum X-dimension for an "open system"
        (a bar code label that will be read by scanners from
        outside your company) is 7.5 mils.

        """
        _rv = max(sum(sequence) * xdim * .15 / 1000, .25) * 72
        return int(math.ceil(_rv))

    def check_digit(self, text, errors="strict"):
        """Compute check digit for given text

        Parameters:
            text: string to encode
            errors: error handling scheme: "strict" or "ignore".

        Return value: check digit character.

        """
        raise NotImplementedError

class Code2of5i(BarCode):

    """Interleaved 2 of 5

    Interleaved 2 of 5 is a a numbers-only bar code.
    The code is a high density code that can hold up to 18
    digits per inch when printed using a 7.5 mil X dimension.
    A check digit is optional.

    The height of the bars must be at least .15 times the symbol's length
    (not counting quiet zones) or .25 inches, whichever is larger.

    It is recommended to use bearer bars and/or check digit
    and/or fixed symbol length to protect against partial scans.
    The bearer bar must touch the top and bottom of all the bars
    and must be at least 3X wide.

    Check sum calculation:

        1.Identify even and odd positioned characters in the message
            with the right-hand message character ALWAYS defined as
            an even positioned character.

        2. Sum the numeric values of the odd positioned characters.

        3. Sum the numeric values of the even positioned characters
            and multiply the total value by three.

        4. Sum the odd and even totals from steps 2 and 3.

        5. Determine the smallest number which, when added to the sum
            in step 4, will result in a multiple of 10. This number is
            the value of the checksum character.

        6. If Interleaved 2 of 5 code is being used, determine whether
            the total number of characters (message plus checksum)
            is odd or even. If odd, add a leading, non significant zero
            to the message to produce an even number of total characters
            as required by the symbology.

    Encoding examples:

    >>> code2of5i("25")
    (1, 1, 1, 1, 1, 3, 3, 1, 1, 3, 1, 1, 3, 1, 3, 1, 1)
    >>> code2of5i("5")
    (1, 1, 1, 1, 1, 3, 1, 1, 3, 3, 3, 1, 1, 1, 3, 1, 1)
    >>> print textwrap.fill(repr(code2of5i("19980726")), 64)
    (1, 1, 1, 1, 3, 1, 1, 3, 1, 1, 1, 3, 3, 1, 1, 3, 3, 1, 1, 1, 3,
    3, 1, 1, 1, 1, 1, 1, 3, 1, 3, 3, 1, 3, 1, 1, 3, 3, 1, 3, 1, 1,
    3, 1, 3, 1, 1)

    Check digit examples:

    >>> code2of5i.check_digit("1")
    '7'
    >>> code2of5i.check_digit("12")
    '3'
    >>> code2of5i.check_digit("1234567890")
    '5'

    """

    # default wide-to-narrow multiple
    W2N = 3

    PATTERNS = (
        # 0 for narrow element, 1 for wide one
        (0, 0, 1, 1, 0), # 0
        (1, 0, 0, 0, 1), # 1
        (0, 1, 0, 0, 1), # 2
        (1, 1, 0, 0, 0), # 3
        (0, 0, 1, 0, 1), # 4
        (1, 0, 1, 0, 0), # 5
        (0, 1, 1, 0, 0), # 6
        (0, 0, 0, 1, 1), # 7
        (1, 0, 0, 1, 0), # 8
        (0, 1, 0, 1, 0), # 9
    )
    START = (0, 0, 0, 0)
    STOP = (1, 0, 0)

    def __init__(self, w2n=None):
        """Initialize encoder

        Parameters:
            w2n: optional numeric value for wide-to-narrow multiple.
                Must be between 2 and 3 if X dimension is greater than 20mils.
                If X dimension is less than 20 mils, ratio must exceed 2.2.

        """
        super(Code2of5i, self).__init__()
        if w2n is None:
            self.w2n = self.W2N
        else:
            self.w2n = w2n

    def _clean(self, text, errors):
        """Clean the text for encoding

        If errors == "strict", raise error when text contains
        invalid character.  If errors == "ignore", return the
        text with all invalid characters removed.

        """
        if errors == "ignore":
            return _re_nondigit.sub("", text)
        elif _re_nondigit.search(text):
            raise InvalidLiteral(text, self)
        else:
            return text

    def __call__(self, text, errors="strict"):
        # ensure that the text contains only digits
        _text = self._clean(text, errors)
        # pad with zero if necessary
        if len(_text) & 1:
            _text = "0" + _text
        # encode text
        _seq = []
        for _pair in zip(_text[::2], _text[1::2]):
            _seq.extend(itertools.chain(
                *zip(*[self.PATTERNS[int(_digit)] for _digit in _pair])))
        # add start/stop and encode stripe widths
        _widths = (1, self.w2n)
        _seq = [_widths[_stripe]
            for _stripe in (self.START + tuple(_seq) + self.STOP)]
        return tuple(_seq)

    def check_digit(self, text, errors="strict"):
        """Return the check character for given code text"""
        _text = self._clean(text, errors)
        _odd = (len(_text) & 1)
        _sum = sum([(int(_digit) * 3) for _digit in _text[1-_odd::2]]) \
            + sum([int(_digit) for _digit in _text[_odd::2]])
        return str(10 -(_sum %10))[-1]

code2of5i = Code2of5i()

class Code39(BarCode):

    """Code 39

    Code 39 is an alphanumeric bar code.  It is designed to encode
    26 uppercase letters, 10 digits and 7 special characters.

    The height of the bars must be at least .15 times the symbol's length
    (not counting quiet zones) or .25 inches, whichever is larger.

    Code 39 does not normally include a check character, however there
    is an established check character for applications that need it.
    The value of each data character (0 for zero .. 42 for percent sign)
    is summed up and divided by 43.  The remainder is the value of
    the character to use as the check character.

    Encoding example:

    >>> print textwrap.fill(repr(Code39(gap=2)("BARCODE1")), 64)
    (1, 3, 1, 1, 3, 1, 3, 1, 1, 2, 1, 1, 3, 1, 1, 3, 1, 1, 3, 2, 3,
    1, 1, 1, 1, 3, 1, 1, 3, 2, 3, 1, 1, 1, 1, 1, 3, 3, 1, 2, 3, 1,
    3, 1, 1, 3, 1, 1, 1, 2, 3, 1, 1, 1, 3, 1, 1, 3, 1, 2, 1, 1, 1,
    1, 3, 3, 1, 1, 3, 2, 3, 1, 1, 1, 3, 3, 1, 1, 1, 2, 3, 1, 1, 3,
    1, 1, 1, 1, 3, 2, 1, 3, 1, 1, 3, 1, 3, 1, 1)

    >>> code39.check_digit("BARCODE1")
    'Q'
    >>> code39.check_digit("12345ABCDE/")
    'T'

    """

    CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-. $/+%"

    # default wide-to-narrow multiple
    W2N = 3

    # default intercharacter gap width.
    GAP = 3

    # minimum size of quiet zones, in mils
    QZ_MILS = 100

    PATTERNS = (
        # 0 for narrow element, 1 for wide one
        (0, 0, 0, 1, 1, 0, 1, 0, 0), # 0
        (1, 0, 0, 1, 0, 0, 0, 0, 1), # 1
        (0, 0, 1, 1, 0, 0, 0, 0, 1), # 2
        (1, 0, 1, 1, 0, 0, 0, 0, 0), # 3
        (0, 0, 0, 1, 1, 0, 0, 0, 1), # 4
        (1, 0, 0, 1, 1, 0, 0, 0, 0), # 5
        (0, 0, 1, 1, 1, 0, 0, 0, 0), # 6
        (0, 0, 0, 1, 0, 0, 1, 0, 1), # 7
        (1, 0, 0, 1, 0, 0, 1, 0, 0), # 8
        (0, 0, 1, 1, 0, 0, 1, 0, 0), # 9
        (1, 0, 0, 0, 0, 1, 0, 0, 1), # A
        (0, 0, 1, 0, 0, 1, 0, 0, 1), # B
        (1, 0, 1, 0, 0, 1, 0, 0, 0), # C
        (0, 0, 0, 0, 1, 1, 0, 0, 1), # D
        (1, 0, 0, 0, 1, 1, 0, 0, 0), # E
        (0, 0, 1, 0, 1, 1, 0, 0, 0), # F
        (0, 0, 0, 0, 0, 1, 1, 0, 1), # G
        (1, 0, 0, 0, 0, 1, 1, 0, 0), # H
        (0, 0, 1, 0, 0, 1, 1, 0, 0), # I
        (0, 0, 0, 0, 1, 1, 1, 0, 0), # J
        (1, 0, 0, 0, 0, 0, 0, 1, 1), # K
        (0, 0, 1, 0, 0, 0, 0, 1, 1), # L
        (1, 0, 1, 0, 0, 0, 0, 1, 0), # M
        (0, 0, 0, 0, 1, 0, 0, 1, 1), # N
        (1, 0, 0, 0, 1, 0, 0, 1, 0), # O
        (0, 0, 1, 0, 1, 0, 0, 1, 0), # P
        (0, 0, 0, 0, 0, 0, 1, 1, 1), # Q
        (1, 0, 0, 0, 0, 0, 1, 1, 0), # R
        (0, 0, 1, 0, 0, 0, 1, 1, 0), # S
        (0, 0, 0, 0, 1, 0, 1, 1, 0), # T
        (1, 1, 0, 0, 0, 0, 0, 0, 1), # U
        (0, 1, 1, 0, 0, 0, 0, 0, 1), # V
        (1, 1, 1, 0, 0, 0, 0, 0, 0), # W
        (0, 1, 0, 0, 1, 0, 0, 0, 1), # X
        (1, 1, 0, 0, 1, 0, 0, 0, 0), # Y
        (0, 1, 1, 0, 1, 0, 0, 0, 0), # Z
        (0, 1, 0, 0, 0, 0, 1, 0, 1), # -
        (1, 1, 0, 0, 0, 0, 1, 0, 0), # .
        (0, 1, 1, 0, 0, 0, 1, 0, 0), # space
        (0, 1, 0, 1, 0, 1, 0, 0, 0), # $
        (0, 1, 0, 1, 0, 0, 0, 1, 0), # /
        (0, 1, 0, 0, 0, 1, 0, 1, 0), # +
        (0, 0, 0, 1, 0, 1, 0, 1, 0), # %
    )
    # The * character is used only for the start/stop character.
    ASTERISK = (0, 1, 0, 0, 1, 0, 1, 0, 0)

    def __init__(self, w2n=None, gap=None):
        """Initialize encoder

        Parameters:
            w2n: optional numeric value for wide-to-narrow multiple.
                Must be between 2 and 3 if X dimension is greater than 20mils.
                If X dimension is less than 20 mils, ratio must exceed 2.2.
            gap: optional intercharacter gap (I) width, given a X multiple.
                The maximum value (based on the Code 39 specification)
                for I is 5.3X for X less than 10 mils.  If X is 10 mils
                or greater, the value of I is 3X or 53 mils, whichever
                is greater.  However, for good quality printers,
                I often equals X.

        """
        super(Code39, self).__init__()
        if w2n is None:
            self.w2n = self.W2N
        else:
            self.w2n = w2n
        if gap is None:
            self.gap = self.GAP
        else:
            self.gap = gap

    def _encode_chars(self, text, errors):
        """Return code numbers for all characters in text

        Parameters:
            text: string to encode
            errors: error handling scheme: "strict" or "ignore".

        Return value: list of character codes.

        """
        _rv = []
        for _char in text:
            try:
                _rv.append(self.CHARS.index(_char))
            except ValueError:
                if errors != "ignore":
                    raise InvalidLiteral(text, self)
        return _rv

    def __call__(self, text, errors="strict"):
        _codes = self._encode_chars(text, errors)
        _widths = (1, self.w2n)
        _gap = (self.gap,)
        _asterisk = tuple([_widths[_stripe] for _stripe in self.ASTERISK])
        _seq = _asterisk + _gap + tuple(itertools.chain(*[(
            tuple([_widths[_stripe] for _stripe in self.PATTERNS[_char]])
            + _gap) for _char in _codes])) + _asterisk
        return tuple(_seq)

    def check_digit(self, text, errors="strict"):
        """Return the check character for given code text"""
        _sum = sum(self._encode_chars(text, errors))
        return self.CHARS[_sum % 43]

code39 = Code39()

class Code128(BarCode):

    """Code 128

    Code 128 is a very high density alphanumeric bar code.
    It is designed to encode all 128 ASCII characters, and will use
    the least amount of space for data of 6 characters or more
    of any 1-D symbology.

    The minimum bar height is 15 percent of the symbol length
    or 0.25 inches, whichever is greater.

    The check character is a Modulus 103 Checksum that is calculated
    by summing the start code value plus the product of each character
    position (most significant character position equals 1) and the
    character value of the character at that position.  This sum is
    divided by 103.  The remainder of the answer is the value of the
    Check Character. Every encoded character is included except the
    Stop and Check Character.

    Note: this implementation does not provide API for check digit
    calculation because for symbol composition check digit is
    meaningless without encoding (it includes start code),
    and bar code readers perform the check internally.

    Encoding examples:

    >>> print textwrap.fill(repr(code128("Code 128")), 64)
    (2, 1, 1, 2, 1, 4, 1, 3, 1, 3, 2, 1, 1, 3, 4, 1, 1, 1, 1, 4, 1,
    2, 2, 1, 1, 1, 2, 2, 1, 4, 2, 1, 2, 2, 2, 2, 1, 2, 3, 2, 2, 1,
    2, 2, 3, 2, 1, 1, 3, 1, 1, 2, 2, 2, 1, 1, 1, 4, 2, 2, 2, 3, 3,
    1, 1, 1, 2)
    >>> print textwrap.fill(repr(code128("\rx")), 64)
    (2, 1, 1, 4, 1, 2, 4, 1, 3, 1, 1, 1, 1, 1, 4, 1, 3, 1, 4, 2, 1,
    2, 1, 1, 3, 2, 1, 2, 2, 1, 2, 3, 3, 1, 1, 1, 2)
    >>> print textwrap.fill(repr(code128("0123456789")), 64)
    (2, 1, 1, 2, 3, 2, 2, 2, 2, 1, 2, 2, 3, 1, 2, 1, 3, 1, 1, 1, 3,
    1, 2, 3, 1, 4, 1, 1, 2, 2, 2, 1, 2, 1, 4, 1, 1, 4, 2, 1, 1, 2,
    2, 3, 3, 1, 1, 1, 2)
    >>> print textwrap.fill(repr(code128("01234\\n")), 64)
    (2, 1, 1, 2, 3, 2, 2, 2, 2, 1, 2, 2, 3, 1, 2, 1, 3, 1, 3, 1, 1,
    1, 4, 1, 2, 2, 1, 2, 3, 1, 1, 4, 2, 2, 1, 1, 1, 2, 1, 1, 4, 2,
    2, 3, 3, 1, 1, 1, 2)

    """
    # Note: encoding examples use:
    #   1. Code B
    #   2. Code A, switch to Code B
    #   3. Code C
    #   4. Code C, switch to Code A

    # pylint: disable-msg=W0223
    # W0223: Method 'check_digit' is abstract in class 'BarCode'
    #   but is not overridden - that's intentional (see docstring)

    CHARS_A =" !\"#$%&\'()*+,-./0123456789:;<=>?@" \
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_" \
        "\000\001\002\003\004\005\006\007\010\011\012\013" \
        "\014\015\016\017\020\021\022\023\024\025\026\027" \
        "\030\031\032\033\034\035\036\037"
    CHARS_B =" !\"#$%&\'()*+,-./0123456789:;<=>?@" \
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_" \
        "`abcdefghijklmnopqrstuvwxyz{|}~\177"
    CHARS_C ="0123456789" # not used

    PATTERNS = (
        (2,1,2,2,2,2), (2,2,2,1,2,2), (2,2,2,2,2,1), (1,2,1,2,2,3),
        (1,2,1,3,2,2), (1,3,1,2,2,2), (1,2,2,2,1,3), (1,2,2,3,1,2),
        (1,3,2,2,1,2), (2,2,1,2,1,3), (2,2,1,3,1,2), (2,3,1,2,1,2),
        (1,1,2,2,3,2), (1,2,2,1,3,2), (1,2,2,2,3,1), (1,1,3,2,2,2),
        (1,2,3,1,2,2), (1,2,3,2,2,1), (2,2,3,2,1,1), (2,2,1,1,3,2),
        (2,2,1,2,3,1), (2,1,3,2,1,2), (2,2,3,1,1,2), (3,1,2,1,3,1),
        (3,1,1,2,2,2), (3,2,1,1,2,2), (3,2,1,2,2,1), (3,1,2,2,1,2),
        (3,2,2,1,1,2), (3,2,2,2,1,1), (2,1,2,1,2,3), (2,1,2,3,2,1),
        (2,3,2,1,2,1), (1,1,1,3,2,3), (1,3,1,1,2,3), (1,3,1,3,2,1),
        (1,1,2,3,1,3), (1,3,2,1,1,3), (1,3,2,3,1,1), (2,1,1,3,1,3),
        (2,3,1,1,1,3), (2,3,1,3,1,1), (1,1,2,1,3,3), (1,1,2,3,3,1),
        (1,3,2,1,3,1), (1,1,3,1,2,3), (1,1,3,3,2,1), (1,3,3,1,2,1),
        (3,1,3,1,2,1), (2,1,1,3,3,1), (2,3,1,1,3,1), (2,1,3,1,1,3),
        (2,1,3,3,1,1), (2,1,3,1,3,1), (3,1,1,1,2,3), (3,1,1,3,2,1),
        (3,3,1,1,2,1), (3,1,2,1,1,3), (3,1,2,3,1,1), (3,3,2,1,1,1),
        (3,1,4,1,1,1), (2,2,1,4,1,1), (4,3,1,1,1,1), (1,1,1,2,2,4),
        (1,1,1,4,2,2), (1,2,1,1,2,4), (1,2,1,4,2,1), (1,4,1,1,2,2),
        (1,4,1,2,2,1), (1,1,2,2,1,4), (1,1,2,4,1,2), (1,2,2,1,1,4),
        (1,2,2,4,1,1), (1,4,2,1,1,2), (1,4,2,2,1,1), (2,4,1,2,1,1),
        (2,2,1,1,1,4), (4,1,3,1,1,1), (2,4,1,1,1,2), (1,3,4,1,1,1),
        (1,1,1,2,4,2), (1,2,1,1,4,2), (1,2,1,2,4,1), (1,1,4,2,1,2),
        (1,2,4,1,1,2), (1,2,4,2,1,1), (4,1,1,2,1,2), (4,2,1,1,1,2),
        (4,2,1,2,1,1), (2,1,2,1,4,1), (2,1,4,1,2,1), (4,1,2,1,2,1),
        (1,1,1,1,4,3), (1,1,1,3,4,1), (1,3,1,1,4,1), (1,1,4,1,1,3),
        (1,1,4,3,1,1), (4,1,1,1,1,3), (4,1,1,3,1,1), (1,1,3,1,4,1),
        (1,1,4,1,3,1), (3,1,1,1,4,1), (4,1,1,1,3,1), (2,1,1,4,1,2),
        (2,1,1,2,1,4), (2,1,1,2,3,2),
        (2,3,3,1,1,1,2), # Note: STOP pattern ends with bar, not space
    )

    SHIFT = 98
    CODEC = 99
    CODEB = 100
    CODEA = 101
    START_A = 103
    START_B = 104
    START_C = 105
    STOP = 106

    def _clean(self, text, errors):
        """Clean the text for encoding

        If errors == "strict", raise error when text contains
        invalid character.  If errors == "ignore", return the
        text with all invalid characters removed.

        """
        # digits (set C) are in A and B sets too
        _allchars = self.CHARS_A + self.CHARS_B
        if errors == "ignore":
            return "".join([_char for _char in text if _char in _allchars])
        else:
            for _char in text:
                if _char not in _allchars:
                    raise InvalidLiteral(text, self)
            return text

    @staticmethod
    def _encode_ab(text, chars):
        """Encode text with character set A or B"""
        _rv = []
        # Note: the speed may be improved by moving try/except
        # outside the loop (suggested by yarcat):
        #    try:
        #        for _char in text:
        #            _rv.append(chars.index(_char))
        #    except ValueError:
        #        pass
        for _char in text:
            try:
                _code = chars.index(_char)
            except ValueError:
                # character not in this set
                break
            else:
                _rv.append(_code)
        return _rv

    def _encode(self, text):
        """Encode a text string

        Return value: a list starting from CODEC or CODEB or CODEA
        and containing all text characters encoded to Code 128 values.

        """
        # output sequences for all code sets
        _seq_a = []
        _seq_b = []
        _seq_c = []
        # look for starting sequence containing only digits (Code C)
        _match = _re_nondigit.search(text)
        if _match is None:
            # the text contains only digits.
            _len_c = len(text)
        else:
            _len_c = _match.start()
        # Code C is the best of three when there are 4 or more digits
        if _len_c > 3:
            # Code C length must be even
            _len_c &= ~1
            # A and B are known to be worse
            _len_a = _len_b = 0
            # encode digits
            _seq_c = [int(text[_idx:_idx+2]) for _idx in xrange(0, _len_c, 2)]
        else:
            # no characters will be encoded with Code C
            _len_c = 0
            _seq_a = self._encode_ab(text, self.CHARS_A)
            _seq_b = self._encode_ab(text, self.CHARS_B)
            _len_a = len(_seq_a)
            _len_b = len(_seq_b)
        # select the winner
        (_len, _code, _seq) = max([
            (_len_a, self.CODEA, _seq_a),
            (_len_b, self.CODEB, _seq_b),
            (_len_c, self.CODEC, _seq_c),
        ])
        _seq.insert(0, _code)
        _tail = text[_len:]
        if _tail:
            _seq.extend(self._encode(_tail))
        return _seq

    def __call__(self, text, errors="strict"):
        _seq = self._encode(self._clean(text, errors))
        # replace code selection character with start character
        _code = _seq.pop(0)
        if _code == self.CODEC:
            _code = self.START_C
        elif _code == self.CODEA:
            _code = self.START_A
        else: # self.CODEB:
            _code = self.START_B
        # compute checksum
        _sum = _code + sum([(_char * (_idx + 1))
            for (_idx, _char) in enumerate(_seq)])
        # append start code, check digit and stop code
        _seq = [_code] + _seq + [(_sum % 103), self.STOP]
        # recode to bar/space patterns
        _seq = tuple(itertools.chain(*[self.PATTERNS[_char]
            for _char in _seq]))
        return _seq

code128 = Code128()

def _test():
    """Run doctests"""
    import doctest
    # textwrap is used in tests to wrap output
    # so that example lines do not exceed allowed
    # source code width.
    import textwrap
    (_fail, _total) = doctest.testmod(extraglobs={"textwrap": textwrap})
    # if there were failed tests, doctest reported that itself
    if not _fail:
        print "%i tests passed." % _total

if __name__ == "__main__":
    _test()

# vim: set et sts=4 sw=4 :
