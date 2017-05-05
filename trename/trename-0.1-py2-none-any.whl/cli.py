import argparse
from trename import trename
from os import rename


def main():
    p = argparse.ArgumentParser(prog='trename')
    p.add_argument('-v', '--verbose', action='store_true', help='print old name and new name for each file ')
    p.add_argument('-n', '--dry-run', action='store_true', help='print names, do not actually rename')
    p.add_argument('-D', '--debug', action='store_true', help='print debug information')
    p.add_argument('from_tpl', help='template for old file name')
    p.add_argument('to_tpl', help='template for new file name')
    p.add_argument('files', nargs='*', help='files that will be renamed')

    args = p.parse_args()

    if args.debug:
        re_in = trename.to_re_in(args.from_tpl)
        re_out = trename.to_re_out(args.to_tpl)
        print('Regexp from: "{}"\nRegexp to:   "{}"'.format(re_in, re_out))

    try:
        trename.validate_patterns(args.from_tpl, args.to_tpl)
        for filename in args.files:
            if args.debug:
                print("Trying: " + filename)
            try:
                to_filename = trename.new_name(filename, args.from_tpl, args.to_tpl)
            except trename.NoMatchException:
                continue

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
    except trename.IdentifiersNotFound as ex:
        print("Invalid pattern: identifiers not found in from_tpl: {}".format(
            ', '.join(ex.identifiers)
        ))


if __name__ == '__main__':
    main()