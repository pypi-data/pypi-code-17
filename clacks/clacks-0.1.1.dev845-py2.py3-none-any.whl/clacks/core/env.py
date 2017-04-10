#!/usr/bin/env python3

"""Basic constants and functions needed in most of the code.

Imported to gtcms.core for convenience.
"""

import os
import sys
from pathlib import Path
from subprocess import PIPE, Popen

__all__ = ['hostname', 'lang', 'revision', 'version', 'ROOTPATH', 'MODE',
           'fullPath', 'resolvePath']


ROOTPATH = Path(os.environ.get('GTOOL_ENVPATH', sys.prefix)).resolve()
MODE = os.environ.get('GTMODE', 'production')

if str(ROOTPATH) == sys.base_prefix:
    raise Exception('dedicated virtual environment or'
                    ' GTOOL_ENVPATH enviromnent variable'
                    ' pointing to project root directory needed')


def resolvePath(*parts):
    """Create path validated to be contained in project ROOTPATH"""

    result = Path(ROOTPATH, *parts)

    if result.exists():
        result = result.resolve()  # pylint: disable=redefined-variable-type
    elif '..' in result.parts:
        raise ValueError('path contains insecure /../ parts')
    elif not result.is_absolute():
        return result

    if result.parts[:len(ROOTPATH.parts)] != ROOTPATH.parts:
        raise ValueError('path goes outside of project tree')

    return result


def fullPath(*parts):  # obsolete
    """Obsolete, use resolvePath() instead."""
    return str(resolvePath(*parts))


def hostname():
    """Return current host name."""
    return os.uname()[1]


def lang():
    """Not implemented yet, returns 'pl' for now."""
    return 'pl'


def revision():
    """return local revision number from Mercurial
    or ./config/_build.json.

    TODO: probably should return revision hash as well?
    """
    from . import Cache

    def _revision():
        """really fetch revision number"""
        import json
        with open(os.devnull, 'w') as NULL:
            repodata = [a.split(':')[1].strip()
                        for a in Popen(['hg', 'summary'],
                                       cwd=str(ROOTPATH),
                                       stdout=PIPE,
                                       stderr=NULL)
                        .communicate()[0].decode().split('\n')
                        if a.startswith('parent:')]
        if len(repodata):
            return repodata[0]
        else:
            try:
                return json.load((ROOTPATH/'config/_build.json').open('r'))['revision']
            except:  # pylint: disable=bare-except
                return '0'

    return Cache.get('hg-local-revision', callback=_revision)


def version():
    """
    Currently project version is derived from last commit date
    for major and minor number by using year and month accordingly
    and appending Mercurial local revision number (which sometimes
    may differ between instances due to different push/pull order)
    """
    from . import Cache

    def _version():
        """Construct version from Mercurial last commit date and revision if available."""
        from time import strptime
        import json
        rev = '0'
        date = None
        with open(os.devnull, 'w') as NULL:
            for a in Popen(['hg', 'parent'],
                           cwd=str(ROOTPATH),
                           stdout=PIPE,
                           stderr=NULL).communicate()[0].decode().split('\n'):
                if a.startswith('changeset:'):
                    rev = a.split(':')[1].strip()
                if a.startswith('date:'):
                    date = strptime(a[5:-6].strip())
        if date:
            return '%d.%d.%s' % (date.tm_year % 100, date.tm_mon, rev)
        else:
            try:
                info = json.load((ROOTPATH/'config/_build.json').open('r'))
                date = strptime(info['date'][:-6].strip())
                return '%d.%d.%s' % (date.tm_year % 100, date.tm_mon, info['revision'])
            except FileNotFoundError:
                return '0.0.0'

    return Cache.get('hg-local-version', callback=_version)
