import re
import logging
import csv, io
import datetime, sys, os
import email
import shlex, subprocess, json
import pathlib
import horetu
import horetu.types as t
from collections import OrderedDict
from pprint import pformat
from enum import Enum
from string import Formatter
from email.policy import SMTPUTF8
from functools import partial
from collections import defaultdict, Counter
from . import util

logger = logging.getLogger(__name__)

def FileOrDir(x):
    if os.path.isfile(x):
        y = x
    else:
        y = t.InputDirectory(x)
    return pathlib.Path(y)

def _format_konftel(_, persons):
    '''
    Format for phone box import to the Konftel 300IP.
    '''
    fp = io.StringIO()
    w = csv.DictWriter(fp, fieldnames=['Name', 'Number'], delimiter=';')
    w.writeheader()
    for person in persons:
        if ('name-latin' in person or 'name' in person) and 'phone' in person:
            w.writerow({
                'Name': person.get('name-latin', person['name']),
                'Number': person['phone-numeric'].replace(' ', ''),
            })
    
    fp.seek(0)
    for row in fp:
        stripped = row.replace('\r', '').rstrip('\n')
        try:
            encoded = stripped.encode('latin1')
        except UnicodeEncodeError:
            msg = 'Could not encode as latin1, skipping: %s'
            logger.warning(msg % stripped)
        else:
            yield encoded

def _format_python(_, persons):
    '''
    Format for phone box import to the Konftel 300IP.
    '''
    return pformat(list(persons))

def from_template(*formats, encoding='utf-8'):
    '''
    Produce an output formatter that attempts to format with a series of
    templates, using the first one that works.

    :param str formats: Python string formatting template for one line
        of the output file
    '''
    def formatter(strsep, persons):
        first = True
        for person in persons:
            for sub_format in formats:
                m = _multi_keys(sub_format)
                sub_persons = []
                if len(m) == 0:
                    sub_persons.append(person)
                elif len(m) == 1:
                    k = list(m)[0]
                    for value in person.get(k, []):
                        sub_persons.append(dict(person))
                        sub_persons[-1][k] = value
                else:
                    raise NotImplementedError('Only one multi-key is allowed at a time.')

                try:
                    for sub_person in sub_persons:
                        line_str = sub_format.format(**sub_person)
                        try:
                            line_bytes = line_str.encode(encoding)
                        except UnicodeEncodeError:
                            msg = 'Could not encode as %s: %s'
                            logger.warning(msg % (encoding, line_str))
                            line_bytes = util.as_7bit(line_str).encode(encoding)
                        if strsep:
                            if first:
                                first = False
                            else:
                                yield strsep.encode(encoding)
                        yield line_bytes
                except KeyError as e:
                    header = e.args[0]
                    if header not in headers:
                        raise horetu.Error('Bad string format variable: %s' % header)
                else:
                    break
    return formatter

def _multi_keys(sub_format, f=Formatter()):
    return set(field_name \
        for literal_text, field_name, format_spec, conversion \
        in f.parse(sub_format) \
        if field_name and headers.get(field_name) == H.multi)

def _parse_multi(root):
    if root.is_file():
        paths = [root]
    else:
        paths = root.iterdir()
    for path in paths:
        if not path.name.startswith('.') and path.is_file():
            person = _parse_single(path)
            if root.is_file():
                person['identifier'] = root.name
            else:
                person['identifier'] = path.relative_to(root)
            yield person

def _message(text):
    return email.message_from_string(text, policy=SMTPUTF8)

def _parse_single(path,
                  linebreak=re.compile(r' *[/\r\n]+ *'),
                  nonphone=re.compile(r'[^0-9]')):
    person = _message(path.read_text())
    person_headers = Counter(header.lower() for header in person)
    if set(h for h in person_headers if not h.startswith('x-')).issubset(headers):
        out = {}
        for header_name, header_count in headers.items():
            if header_name in person_headers:
                if header_count == H.single:
                    xs = person.get_all(header_name)
                    if len(xs) == 1:
                        out[header_name] = xs[0]
                    elif len(xs) > 1:
                        raise horetu.Error('%s: Only one %s value is allowed' % \
                                           (path, header_name))
                elif header_count == H.multi:
                    out[header_name] = person.get_all(header_name)

        if 'post' in out:
            post_lines = [out.get('name', 'identifier')] + re.split(linebreak, out['post'])
            out['post-formatted'] = '\n'.join(post_lines)

        if 'phone' in out:
            out['phone-numeric'] = re.sub(nonphone, '', out['phone'])

        return out
    else:
        raise horetu.Error('%s: Only these keys are allowed: %s' % \
                           (path, str(headers)))

formats = OrderedDict([
    ('mh', from_template(
        '{identifier}: {name} <{email}>',
        '{identifier}: {email}',
    )),
    ('mutt', from_template(
        'alias {identifier} {name} <{email}>',
        'alias {identifier} {email}',
    )),
    ('newsbeuter', from_template(
        '{feed} "~{name}"',
        '{feed}',
    )),
    ('konftel', _format_konftel),

    ('python', _format_python),
    ('custom', None),
])

class H(Enum):
    single = 1
    multi = 2
    custom = 3

headers = {
    'name': H.single,
    'name-latin': H.single,
    'phone': H.single, 'email': H.single, 'post': H.single,
    'feed': H.multi, 'web': H.multi,

    'phone-numeric': H.single, 'post-formatted': H.single,
}

def format():
    '''
    Print a list of the arguments that are available for string
    formatting.
    '''
    return sorted(headers)

def dump(contact: FileOrDir,
         output_format: formats=formats['python'], custom_format='', *,
         separator=None):
    if not output_format:
        output_format = from_template(custom_format)
    return output_format(separator, _parse_multi(contact))
dump.__doc__ = '''
Convert from a contact file to a different format.

:param contact: A contact file or a directory of contact files
:param output_format: One of "%s", defaults to "python"
:param custom_format: Python format string used when output_format is
    "custom", for example, "{identifier}: {phone}"
:param separator: Insert this text as a separator line between contacts in the
    output. This can be helpful if if the output for a particular
    contact may span multiple lines.
:rtype: iter
:returns: Iterable of str output chunked by line
''' % '", "'.join(formats)

