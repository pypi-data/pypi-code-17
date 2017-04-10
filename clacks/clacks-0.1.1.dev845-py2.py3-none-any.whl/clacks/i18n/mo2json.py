#!/usr/bin/env python3

"""
simple python script to convert gettext .mo file to a .json file for jQuery plugin
usage: mo2json.py DOMAIN PATH LANG
for example: $ bin/mo2json.py main ./locale/ pl
"""

import gettext
import json
import sys

from collections import OrderedDict


def convert(domain, path, lang=None, indent=False):
    """converts gettext compiled mo file to JSON dictionary"""
    if lang is None:
        lang = []
    tr = gettext.translation(domain, path, lang)
    # for unknown reasons, instead of having plural entries like
    # key: [sg, pl1...]x
    # tr._catalog has (key, n): pln,

    # just for aesthetics
    result = OrderedDict()
    # sorting by repr is "good enough" as there's no language with more than 6 plural forms
    for msgid, msgstr in sorted(tr._catalog.items(), key=repr):  # pylint: disable=no-member
        if isinstance(msgid, tuple):
            if msgid[0] not in result:
                result[msgid[0]] = [msgstr]
            else:
                result[msgid[0]].append(msgstr)
        elif msgid == '':
            result[''] = {'lang': lang[0], 'domain': domain}
            result[''].update({k.lower().replace('-', '_'): v.lstrip()
                               for k, v in (t.split(':', 1) for t in msgstr.split('\n') if ':' in t)
                               if k.lower() in ('plural-forms', 'lang', 'domain')})
        else:
            result[msgid] = [msgstr]  # jed requires to use array also for single translation
    return json.dumps(result, ensure_ascii=False, indent=indent)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Invalid number of arguments")
        exit(1)
    sys.stdout.write(convert(sys.argv[1], sys.argv[2], [sys.argv[3]], True).encode('utf-8'))
