# encoding: utf-8

"""
convert.py

Created by Hywel Thomas on 2010-11-24.
Copyright (c) 2010 Hywel Thomas. All rights reserved.
"""

import inspect
import datetime
import time

import logging_helper
from timingsutil.timers import tz_adjust

__author__ = u'Hywel Thomas'
__copyright__ = u'Copyright (C) 2016 Hywel Thomas'

logging = logging_helper.setup_logging()


def convert(value,
            conversion):
    """
    Used to convert a value using the supplied conversion function
    :param value: value to convert
    :param conversion: conversion function dictionary

    The conversion dictionary can hold a function and its parameters e.g:

        {u'Function': epoch_to_time,
         u'format'  : u'%Y-%m-%d\n%H:%M'}

    might be used for calling the function

       def epoch_to_time(ep = None,
                         format = u'%d-%m-%y %H:%M:%S')

    value is used as the the first parameter

        convert(value = datetime.now(),
                conversion = {u'Function': epoch_to_time,
                              u'format'  : u'%d-%m-%y'}
                )

    is equivalent to calling

        epoch_to_time(datetime.now(),      # without parameter name
                      format = u'%d-%m-%y')

    """
    if conversion is not None:
        try:
            parameters = {key: value
                          for key, value in conversion.iteritems()
                          if key != u'Function'}
            return conversion[u'Function'](value, **parameters)

        except Exception, err:
            if value not in (u'', u'-', u'n/a', None):
                #value = u'ERR({value})'.format(value = unicode(value))
                source = inspect.getsource(conversion[u'Function'])
                logging.exception(u'Failed to convert value ({value}) '
                                  u'using {function}.\n'
                                  u'Parameters: {params}\n'
                                  u'{source}'
                                  .format(value = value,
                                          function = conversion[u'Function'],
                                          params = parameters,
                                          source = source))
    return value


def convert_storage_size(value,
                         units=u'B',
                         output_units=None):

    value = int(value)

    # Validate Units
    supported_units = [u'B',
                       u'KiB', u'KB',
                       u'MiB', u'MB',
                       u'GiB', u'GB',
                       u'TiB', u'TB',
                       u'PiB', u'PB']

    if units not in supported_units:
        raise ValueError(u'{units} is not a recognised unit'
                         .format(units=units))

    elif output_units is not None and output_units not in supported_units:
        raise ValueError(u'{units} is not a recognised unit'
                         .format(units=output_units))

    # Check the multipliers we should be using
    # KB - Kilobyte; KiB - KibiByte
    # 1 KB = 1000 B; 1KiB = 1024 B
    si_multiplier = 1000  # The new system
    iec_multiplier = 1024  # The old system

    input_multiplier = iec_multiplier if u'i' in units else si_multiplier

    if output_units is not None:
        output_multiplier = (iec_multiplier
                             if u'i' in output_units
                             else si_multiplier)
        output_type = u'i' if u'i' in output_units else u''

    else:
        output_multiplier = input_multiplier
        output_type = u'i' if u'i' in units else u''

    # Check for and extract negative
    neg = u'-' if value < 0 else u''
    value = abs(value)

    # Convert input to bytes
    if units == u'B':
        byte_count = value

    elif units in (u'KiB', u'KB'):
        byte_count = value * input_multiplier ** 1

    elif units in (u'MiB', u'MB'):
        byte_count = value * input_multiplier ** 2

    elif units in (u'GiB',  u'GB'):
        byte_count = value * input_multiplier ** 3

    elif units in (u'TiB',  u'TB'):
        byte_count = value * input_multiplier ** 4

    elif units in (u'PiB',  u'PB'):
        byte_count = value * input_multiplier ** 5

    else:
        raise ValueError(u'{units} is not a recognised unit')

    byte_count = float(byte_count)

    # Run the Conversion
    if (byte_count < output_multiplier and output_units is None) or output_units == u'B':
        return u'{neg}{size:.0f}B'.format(neg=neg,
                                          size=byte_count)

    kilobyte_count = byte_count / output_multiplier ** 1
    if (kilobyte_count <= output_multiplier and output_units is None) or output_units in [u'KiB', u'KB']:
        return u'{neg}{size:.1f}K{t}B'.format(neg=neg,
                                              size=kilobyte_count,
                                              t=output_type)

    megabyte_count = byte_count / output_multiplier ** 2
    if (megabyte_count <= output_multiplier and output_units is None) or output_units in [u'MiB', u'MB']:
        return u'{neg}{size:.1f}M{t}B'.format(neg=neg,
                                              size=megabyte_count,
                                              t=output_type)

    gigabyte_count = byte_count / output_multiplier ** 3
    if (gigabyte_count <= output_multiplier and output_units is None) or output_units in [u'GiB', u'GB']:
        return u'{neg}{size:.1f}G{t}B'.format(neg=neg,
                                              size=gigabyte_count,
                                              t=output_type)

    terabyte_count = byte_count / output_multiplier ** 4
    if (terabyte_count <= output_multiplier and output_units is None) or output_units in [u'TiB', u'TB']:
        return u'{neg}{size:.1f}T{t}B'.format(neg=neg,
                                              size=terabyte_count,
                                              t=output_type)

    petabyte_count = byte_count / output_multiplier ** 5
    return u'{neg}{size:.1f}P{t}B'.format(neg=neg,
                                          size=petabyte_count,
                                          t=output_type)


def convert_to_unicode(source_string):

    if not isinstance(source_string, unicode):
        source_string = unicode(source_string)

    return source_string


def datetime_to_epoch(dt=None):

    dt = dt if dt is not None else datetime.datetime.now()

    return (dt - datetime.datetime(1970, 1, 1)).total_seconds() - tz_adjust


def epoch_to_time(ep=None,
                  time_format=u'%d-%m-%y %H:%M:%S'):

    if ep is None:
        ep = datetime_to_epoch(datetime.datetime.now())

    if ep > 9999999999:
        ep /= 1000

    return time.strftime(time_format, time.localtime(ep))


DAYS = (u'Monday',
        u'Tuesday',
        u'Wednesday',
        u'Thursday',
        u'Friday',
        u'Saturday',
        u'Sunday')

MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = DAYS


def day_of_week(ep = None):
    if ep is None:
         ep = time.mktime(datetime.datetime.now().timetuple())
    if ep > 9999999999:
         ep = ep / 1000
    return DAYS[time.localtime(ep).tm_wday]


def next_day(day):
    return DAYS[(DAYS.index(day) + 1) % len(DAYS)]

if __name__ == u"__main__":
    assert next_day(u'Monday') == u'Tuesday'
    assert next_day(u'Sunday') == u'Monday'


def get_datetime_conversion(datetime_format):
    return {u'Function': epoch_to_time,
            u'time_format': datetime_format}


FULL_WIDTH_TABLE = {u' ':      {u'code': u'U+3000', u'wide char': u"\u3000",  u'name': u'IDEOGRAPHIC SPACE'},
                    u'!':      {u'code': u'U+FF01', u'wide char': u'！',      u'name': u'FULLWIDTH EXCLAMATION MARK'},
                    u'"':      {u'code': u'U+FF02', u'wide char': u'＂',      u'name': u'FULLWIDTH QUOTATION MARK'},
                    u'#':      {u'code': u'U+FF03', u'wide char': u'＃',      u'name': u'FULLWIDTH NUMBER SIGN'},
                    u'$':      {u'code': u'U+FF04', u'wide char': u'＄',      u'name': u'FULLWIDTH DOLLAR SIGN'},
                    u'%':      {u'code': u'U+FF05', u'wide char': u'％',      u'name': u'FULLWIDTH PERCENT SIGN'},
                    u'&':      {u'code': u'U+FF06', u'wide char': u'＆',      u'name': u'FULLWIDTH AMPERSAND'},
                    u"'":      {u'code': u'U+FF07', u'wide char': u'＇',      u'name': u'FULLWIDTH APOSTROPHE'},
                    u'(':      {u'code': u'U+FF08', u'wide char': u'（',      u'name': u'FULLWIDTH LEFT PARENTHESIS'},
                    u')':      {u'code': u'U+FF09', u'wide char': u'）',      u'name': u'FULLWIDTH RIGHT PARENTHESIS'},
                    u'*':      {u'code': u'U+FF0A', u'wide char': u'＊',      u'name': u'FULLWIDTH ASTERISK'},
                    u'+':      {u'code': u'U+FF0B', u'wide char': u'＋',      u'name': u'FULLWIDTH PLUS SIGN'},
                    u',':      {u'code': u'U+FF0C', u'wide char': u'，',      u'name': u'FULLWIDTH COMMA'},
                    u'-':      {u'code': u'U+FF0D', u'wide char': u'－',      u'name': u'FULLWIDTH HYPHEN-MINUS'},
                    u'.':      {u'code': u'U+FF0E', u'wide char': u'．',      u'name': u'FULLWIDTH FULL STOP'},
                    u'/':      {u'code': u'U+FF0F', u'wide char': u'／',      u'name': u'FULLWIDTH SOLIDUS'},
                    u'0':      {u'code': u'U+FF10', u'wide char': u'０',      u'name': u'FULLWIDTH DIGIT ZERO'},
                    u'1':      {u'code': u'U+FF11', u'wide char': u'１',      u'name': u'FULLWIDTH DIGIT ONE'},
                    u'2':      {u'code': u'U+FF12', u'wide char': u'２',      u'name': u'FULLWIDTH DIGIT TWO'},
                    u'3':      {u'code': u'U+FF13', u'wide char': u'３',      u'name': u'FULLWIDTH DIGIT THREE'},
                    u'4':      {u'code': u'U+FF14', u'wide char': u'４',      u'name': u'FULLWIDTH DIGIT FOUR'},
                    u'5':      {u'code': u'U+FF15', u'wide char': u'５',      u'name': u'FULLWIDTH DIGIT FIVE'},
                    u'6':      {u'code': u'U+FF16', u'wide char': u'６',      u'name': u'FULLWIDTH DIGIT SIX'},
                    u'7':      {u'code': u'U+FF17', u'wide char': u'７',      u'name': u'FULLWIDTH DIGIT SEVEN'},
                    u'8':      {u'code': u'U+FF18', u'wide char': u'８',      u'name': u'FULLWIDTH DIGIT EIGHT'},
                    u'9':      {u'code': u'U+FF19', u'wide char': u'９',      u'name': u'FULLWIDTH DIGIT NINE'},
                    u':':      {u'code': u'U+FF1A', u'wide char': u'：',      u'name': u'FULLWIDTH COLON'},
                    u';':      {u'code': u'U+FF1B', u'wide char': u'；',      u'name': u'FULLWIDTH SEMICOLON'},
                    u'<':      {u'code': u'U+FF1C', u'wide char': u'＜',      u'name': u'FULLWIDTH LESS-THAN SIGN'},
                    u'=':      {u'code': u'U+FF1D', u'wide char': u'＝',      u'name': u'FULLWIDTH EQUALS SIGN'},
                    u'>':      {u'code': u'U+FF1E', u'wide char': u'＞',      u'name': u'FULLWIDTH GREATER-THAN SIGN'},
                    u'?':      {u'code': u'U+FF1F', u'wide char': u'？',      u'name': u'FULLWIDTH QUESTION MARK'},
                    u'@':      {u'code': u'U+FF20', u'wide char': u'＠',      u'name': u'FULLWIDTH COMMERCIAL AT'},
                    u'A':      {u'code': u'U+FF21', u'wide char': u'Ａ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER A'},
                    u'B':      {u'code': u'U+FF22', u'wide char': u'Ｂ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER B'},
                    u'C':      {u'code': u'U+FF23', u'wide char': u'Ｃ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER C'},
                    u'D':      {u'code': u'U+FF24', u'wide char': u'Ｄ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER D'},
                    u'E':      {u'code': u'U+FF25', u'wide char': u'Ｅ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER E'},
                    u'F':      {u'code': u'U+FF26', u'wide char': u'Ｆ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER F'},
                    u'G':      {u'code': u'U+FF27', u'wide char': u'Ｇ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER G'},
                    u'H':      {u'code': u'U+FF28', u'wide char': u'Ｈ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER H'},
                    u'I':      {u'code': u'U+FF29', u'wide char': u'Ｉ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER I'},
                    u'J':      {u'code': u'U+FF2A', u'wide char': u'Ｊ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER J'},
                    u'K':      {u'code': u'U+FF2B', u'wide char': u'Ｋ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER K'},
                    u'L':      {u'code': u'U+FF2C', u'wide char': u'Ｌ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER L'},
                    u'M':      {u'code': u'U+FF2D', u'wide char': u'Ｍ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER M'},
                    u'N':      {u'code': u'U+FF2E', u'wide char': u'Ｎ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER N'},
                    u'O':      {u'code': u'U+FF2F', u'wide char': u'Ｏ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER O'},
                    u'P':      {u'code': u'U+FF30', u'wide char': u'Ｐ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER P'},
                    u'Q':      {u'code': u'U+FF31', u'wide char': u'Ｑ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER Q'},
                    u'R':      {u'code': u'U+FF32', u'wide char': u'Ｒ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER R'},
                    u'S':      {u'code': u'U+FF33', u'wide char': u'Ｓ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER S'},
                    u'T':      {u'code': u'U+FF34', u'wide char': u'Ｔ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER T'},
                    u'U':      {u'code': u'U+FF35', u'wide char': u'Ｕ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER U'},
                    u'V':      {u'code': u'U+FF36', u'wide char': u'Ｖ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER V'},
                    u'W':      {u'code': u'U+FF37', u'wide char': u'Ｗ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER W'},
                    u'X':      {u'code': u'U+FF38', u'wide char': u'Ｘ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER X'},
                    u'Y':      {u'code': u'U+FF39', u'wide char': u'Ｙ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER Y'},
                    u'Z':      {u'code': u'U+FF3A', u'wide char': u'Ｚ',      u'name': u'FULLWIDTH LATIN CAPITAL LETTER Z'},
                    u'[':      {u'code': u'U+FF3B', u'wide char': u'［',      u'name': u'FULLWIDTH LEFT SQUARE BRACKET'},
                    u'\\':     {u'code': u'U+FF3C', u'wide char': u'＼',      u'name': u'FULLWIDTH REVERSE SOLIDUS'},
                    u']':      {u'code': u'U+FF3D', u'wide char': u'］',      u'name': u'FULLWIDTH RIGHT SQUARE BRACKET'},
                    u"\u0302": {u'code': u'U+FF3E', u'wide char': u'＾',      u'name': u'FULLWIDTH CIRCUMFLEX ACCENT'},
                    u'_':      {u'code': u'U+FF3F', u'wide char': u'＿',      u'name': u'FULLWIDTH LOW LINE'},
                    u"\u0060": {u'code': u'U+FF40', u'wide char': u'｀',      u'name': u'FULLWIDTH GRAVE ACCENT'},
                    u'a':      {u'code': u'U+FF41', u'wide char': u'ａ',      u'name': u'FULLWIDTH LATIN SMALL LETTER A'},
                    u'b':      {u'code': u'U+FF42', u'wide char': u'ｂ',      u'name': u'FULLWIDTH LATIN SMALL LETTER B'},
                    u'c':      {u'code': u'U+FF43', u'wide char': u'ｃ',      u'name': u'FULLWIDTH LATIN SMALL LETTER C'},
                    u'd':      {u'code': u'U+FF44', u'wide char': u'ｄ',      u'name': u'FULLWIDTH LATIN SMALL LETTER D'},
                    u'e':      {u'code': u'U+FF45', u'wide char': u'ｅ',      u'name': u'FULLWIDTH LATIN SMALL LETTER E'},
                    u'f':      {u'code': u'U+FF46', u'wide char': u'ｆ',      u'name': u'FULLWIDTH LATIN SMALL LETTER F'},
                    u'g':      {u'code': u'U+FF47', u'wide char': u'ｇ',      u'name': u'FULLWIDTH LATIN SMALL LETTER G'},
                    u'h':      {u'code': u'U+FF48', u'wide char': u'ｈ',      u'name': u'FULLWIDTH LATIN SMALL LETTER H'},
                    u'i':      {u'code': u'U+FF49', u'wide char': u'ｉ',      u'name': u'FULLWIDTH LATIN SMALL LETTER I'},
                    u'j':      {u'code': u'U+FF4A', u'wide char': u'ｊ',      u'name': u'FULLWIDTH LATIN SMALL LETTER J'},
                    u'k':      {u'code': u'U+FF4B', u'wide char': u'ｋ',      u'name': u'FULLWIDTH LATIN SMALL LETTER K'},
                    u'l':      {u'code': u'U+FF4C', u'wide char': u'ｌ',      u'name': u'FULLWIDTH LATIN SMALL LETTER L'},
                    u'm':      {u'code': u'U+FF4D', u'wide char': u'ｍ',      u'name': u'FULLWIDTH LATIN SMALL LETTER M'},
                    u'n':      {u'code': u'U+FF4E', u'wide char': u'ｎ',      u'name': u'FULLWIDTH LATIN SMALL LETTER N'},
                    u'o':      {u'code': u'U+FF4F', u'wide char': u'ｏ',      u'name': u'FULLWIDTH LATIN SMALL LETTER O'},
                    u'p':      {u'code': u'U+FF50', u'wide char': u'ｐ',      u'name': u'FULLWIDTH LATIN SMALL LETTER P'},
                    u'q':      {u'code': u'U+FF51', u'wide char': u'ｑ',      u'name': u'FULLWIDTH LATIN SMALL LETTER Q'},
                    u'r':      {u'code': u'U+FF52', u'wide char': u'ｒ',      u'name': u'FULLWIDTH LATIN SMALL LETTER R'},
                    u's':      {u'code': u'U+FF53', u'wide char': u'ｓ',      u'name': u'FULLWIDTH LATIN SMALL LETTER S'},
                    u't':      {u'code': u'U+FF54', u'wide char': u'ｔ',      u'name': u'FULLWIDTH LATIN SMALL LETTER T'},
                    u'u':      {u'code': u'U+FF55', u'wide char': u'ｕ',      u'name': u'FULLWIDTH LATIN SMALL LETTER U'},
                    u'v':      {u'code': u'U+FF56', u'wide char': u'ｖ',      u'name': u'FULLWIDTH LATIN SMALL LETTER V'},
                    u'w':      {u'code': u'U+FF57', u'wide char': u'ｗ',      u'name': u'FULLWIDTH LATIN SMALL LETTER W'},
                    u'x':      {u'code': u'U+FF58', u'wide char': u'ｘ',      u'name': u'FULLWIDTH LATIN SMALL LETTER X'},
                    u'y':      {u'code': u'U+FF59', u'wide char': u'ｙ',      u'name': u'FULLWIDTH LATIN SMALL LETTER Y'},
                    u'z':      {u'code': u'U+FF5A', u'wide char': u'ｚ',      u'name': u'FULLWIDTH LATIN SMALL LETTER Z'},
                    u'{':      {u'code': u'U+FF5B', u'wide char': u'｛',      u'name': u'FULLWIDTH LEFT CURLY BRACKET'},
                    u'|':      {u'code': u'U+FF5C', u'wide char': u'｜',      u'name': u'FULLWIDTH VERTICAL LINE'},
                    u'}':      {u'code': u'U+FF5D', u'wide char': u'｝',      u'name': u'FULLWIDTH RIGHT CURLY BRACKET'},
                    u'~':      {u'code': u'U+FF5E', u'wide char': u'～',      u'name': u'FULLWIDTH TILDE'},
                    u"¢":      {u'code': u'U+FFE0', u'wide char': u'￠',      u'name': u'FULLWIDTH CENT SIGN'},
                    u'£':      {u'code': u'U+FFE1', u'wide char': u'￡',      u'name': u'FULLWIDTH POUND SIGN'},
                    }


def convert_to_full_width_characters(string):
    for char in FULL_WIDTH_TABLE:
        string = string.replace(char,
                                FULL_WIDTH_TABLE[char][u'wide char'])
    return string
