# -*- coding: utf-8 -*-

"""
CacheBlob CLI interface. Fetch or purge items.

Usage:
    cli.py (fetch|purge|purge_any_expired) [INDEX ...]
    cli.py --handler=sqlite (fetch|purge|purge_any_expired) [INDEX ...]
    cli.py --handler=gzip --index_file=index.db (fetch|purge|purge_any_expired) [INDEX ...]
    cli.py --handler=plaintext --directory=data (fetch|purge|purge_any_expired) [INDEX ...]

Options:
    -h --help               Show this screen.
    --version               Show version.
    --handler=<sqlite>      Handler type [default: sqlite]
    --directory=<data>      Directory if applicable [default: data]
    --index_file=<index.db> Index file if applicable [default: index.db]

If no arguments are specified to fetch, all INDEX are fetched. Purge, however,
will not let you purge everything that easily.
"""

import sys
import os
import pprint
import docopt

CURRENT_DIR = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(CURRENT_DIR, "..")))

from cacheblob import Cacheblob
from cacheblob import __version__

import cacheblob.constants as C

def main():
    """Main CLI handler.

    :returns: 0 on success, exits with message otherwise.
    """

    args = docopt.docopt(__doc__, version=__version__)

    if args['--handler'] not in C.IMPLEMENTED_HANDLERS:
        raise ValueError("Handler \"{}\" is not defined".format(args['--handler']))

    cache = Cacheblob.cache(handler=args['--handler'])
    #print("cache is a {}".format(cache))

    if args['--directory']:
        cache.directory = args['--directory']

    if args['fetch']:
        if not len(args['INDEX']):
            for item in cache.fetch_all():
                pprint.pprint(item.__dict__)
        else:
            for index in args['INDEX']:
                item = cache.fetch(index)
                if item is None:
                    print("Item with index \"{}\" not found".format(index))
                else:
                    pprint.pprint(item.__dict__)
    elif args['purge']:
        if not len(args['INDEX']):
            print("Purged items must be specified individually")
        else:
            for index in args['INDEX']:
                result = cache.purge(index)
                if result:
                    print("Purged item with index \"{}\"".format(index))
                else:
                    print("Could not purge item with index \"{}\"".format(index))
    elif args['purge_any_expired']:
        count = cache.purge_any_expired()
        if count == 1:
            print("Purged 1 item")
        else:
            print("Purged {} items".format(count))

    return 0

if __name__ == '__main__':
    main()
