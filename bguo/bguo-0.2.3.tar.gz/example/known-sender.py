#!/usr/bin/env python3
import subprocess, io
import datetime, sys, os
import json
import email
import horetu
import bguo.dump as d
from functools import partial
from collections import defaultdict

def _load(fp):
    return {k: set(v) for k,v in json.load(fp).items()}

def _dump(obj, fp):
    return json.dump({k: list(v) for k,v in obj.items()}, fp,
                     indent=2, separators=(',', ': '))

def known_sender(contacts, message: partial(open, mode='rb')=sys.stdin.buffer, *,
                 default_folder='inbox',
                 rebuild: float=30, tmp='/tmp/known-email-addresses'):
    '''
    Print contacts that match the header. Exit 0 on match and
    1 on no match. I use this in my ~/.maildelivery file to whitelist
    email addresses for spam filtering.

    :param contacts: Directory of bguo contact files.
    :param int rebuild: Force rebuild the search index if the file is
        more than this many days old. This can be a float; use 0.5 to
        rebuild every 12 hours.
    :rtype: iter
    :returns: Iterable of str output chunked by line
    '''
    if os.path.isfile(tmp) and _is_recent(tmp, rebuild):
        with open(tmp) as fp:
            known_aliases = _load(fp)
    else:
        if os.path.isdir(contacts):
            pass
        try:
            _partial_tpl = ':%(email)s'
            tpl = ['%(x-type)s' + _partial_tpl, default_folder + _partial_tpl]
            known_aliases = defaultdict(list)
            for c in d.dump(contacts, tpl):
                k, v = c.split(':', 1)
                known_aliases[k].append(v)
            with open(tmp, 'w') as fp:
                os.chmod(tmp, 0o400)
                _dump(known_aliases, fp)
        except:
            os.remove(tmp)
            raise
    
    source = message.read()

    for sender in email.message_from_bytes(source).get_all('from'):
        for folder in known_aliases:
            for known in known_aliases[folder]:
                if known in sender:
                    _store(source, folder)
                    sys.exit(0)
    sys.exit(1)

def _store(source, folder):
    p = subprocess.Popen(['/usr/local/libexec/rcvstore', '+' + folder],
                         stdin=subprocess.PIPE)
    p.stdin.write(source)
    p.stdin.close()
    p.wait()

def _is_recent(filename, days):
    threshold = datetime.timedelta(days=days)
    created = datetime.datetime.fromtimestamp(os.stat(filename).st_ctime)
    now = datetime.datetime.now()
    return now < created + threshold

if __name__ == '__main__':
    horetu.cli(known_sender)
