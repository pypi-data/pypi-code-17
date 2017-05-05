import argparse
from trename.trename import new_name
from os import rename
import sys


def main():
    p = argparse.ArgumentParser()
    p.add_argument('-v', '--verbose', action='store_true')
    p.add_argument('-n', '--dry-run', action='store_true')
    p.add_argument('from_tpl')
    p.add_argument('to_tpl')
    p.add_argument('files', nargs='*')

    args = p.parse_args()
    for filename in args.files:
        to_filename = new_name(filename, args.from_tpl, args.to_tpl)
        if to_filename is not None:
            if args.dry_run:
                print("{filename} will be renamed to {to_filename}".format(
                    filename=filename,
                    to_filename=to_filename,
                ))
            else:
                rename(filename, to_filename)
                if args.verbose:
                    print("{filename} renamed to {to_filename}".format(
                        filename=filename,
                        to_filename=to_filename,
                    ))


if __name__ == '__main__':
    main()