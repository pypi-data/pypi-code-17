#!/usr/bin/env python
from __future__ import print_function

import sys

from pytoml import dump, load

__all__ = 'main',
__version__ = '0.1.1'


def main():
    argc = len(sys.argv)
    if argc < 2 or argc % 2 == 0:
        print('usage: KEY VALUE [KEY VALUE ...]', file=sys.stderr)
        raise SystemExit(1)
    pairs = zip(sys.argv[1::2], sys.argv[2::2])
    try:
        table = load(sys.stdin)
    except KeyboardInterrupt:
        raise SystemExit(130)
    for k, v in pairs:
        container = table
        keys = k.split('.')
        key_path = ''
        for key in keys[:-1]:
            key_path += (key and '.') + key
            try:
                container = container[key]
            except KeyError:
                print('error: failed to find', key_path, file=sys.stderr)
                raise SystemExit(2)
        try:
            container[keys[-1]] = v
        except KeyError:
            print('error: failed to find', k, file=sys.stderr)
            raise SystemExit(2)
    dump(table, sys.stdout, sort_keys=True)
    raise SystemExit(0)


if __name__ == '__main__':
    main()
