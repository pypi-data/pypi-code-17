import json
import os
import subprocess

import sys

from codeskeleton.cli import colorize


def safe_print(unicodestring):
    # print(str(unicodestring.encode(sys.stdout.encoding, "replace")))
    print(unicodestring)


def print_error(errormessage, prefix=u'ERROR: '):
    safe_print(colorize.colored_text(
        u'{}{}'.format(prefix, errormessage),
        color=colorize.COLOR_RED, bold=True))


def print_warning(warningmessage, prefix=u'WARNING: '):
    safe_print(colorize.colored_text(
        u'{}{}'.format(prefix, warningmessage),
        color=colorize.COLOR_YELLOW, bold=True))


def print_bold(message):
    safe_print(colorize.colored_text(
        message, bold=True))


def print_success(successmessage):
    safe_print(colorize.colored_text(
        successmessage,
        color=colorize.COLOR_GREEN))


def print_blue(message):
    safe_print(colorize.colored_text(
        message,
        color=colorize.COLOR_BLUE))


def exit_with_error(errormessage):
    print_error(errormessage)
    raise SystemExit()


def prettyformat_error(error):
    print_error(error,
                prefix=u'{}: '.format(error.__class__.__name__))


def prettyprint_dict(dct):
    safe_print(json.dumps(dct, indent=2))


def decode_utf8_string(utf8_encoded_bytestring):
    return utf8_encoded_bytestring.decode('utf-8')


def open_file_with_default_os_opener(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        if sys.platform == "darwin":
            opener = "open"
        else:
            opener = "xdg-open"
        subprocess.call([opener, filename])


def confirm(message):
    safe_print(colorize.colored_text(
        message, color=colorize.COLOR_RED, bold=True))
    return str(input('[y/N] ')).strip().lower() == 'y'
