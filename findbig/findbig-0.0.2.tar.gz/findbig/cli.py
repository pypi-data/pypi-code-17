#!/usr/bin/env python3
from os import walk, environ
from os.path import join, getsize, normpath, islink
import sys
from argparse import ArgumentParser


unit_sizes = {
    "b": 1024 ** 0,
    "k": 10 ** 3,
    "m": 10 ** 6,
    "g": 10 ** 9,
    "t": 10 ** 12
}

# This used to be MB, GB, etc, but now it seems pointless
unit_names = {
    "b": "B",
    "k": "K",
    "m": "M",
    "g": "G",
    "t": "T"
}


def find_files(base_dir, min_size=0, verbose=False):
    for current_dir, subdirs, files in walk(base_dir):
        for file_name in files:
            file_path = normpath(join(current_dir, file_name))
            if not islink(file_path):
                try:
                    file_size = getsize(file_path)
                except FileNotFoundError:
                    # File disappeared or dangling link
                    continue
                if file_size < min_size:
                    continue
                yield (file_path, file_size)


def size_to_units(size, unit, round_places=0):
    size = round(size / unit_sizes[unit], round_places)
    if round_places == 0:
        return int(size)
    return size


def main():
    environ["LANG"] = "en_US.UTF-8"
    clean = True
    parser = ArgumentParser(description="Find large files in a directory")
    parser.add_argument("base_dir", help="Root dir to begin search")

    output_opts = parser.add_argument_group("output options")
    output_opts.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    output_opts.add_argument("-f", "--format", default="{fsize}{unit}\t{fpath}", help="Output format")
    output_opts.add_argument("-l", "--limit", type=int, help="Limit result count")
    output_opts.add_argument("-u", "--unit", choices=unit_sizes.keys(), default="b",
                             help="Convert sizes to unit")
    output_opts.add_argument("-r", "--round", type=int, default=0, help="Number of places to round to")
    output_opts.add_argument("-m", "--min-size", default="0", help="Ignore files smaller than threshold")

    args = parser.parse_args()

    min_size = 0
    if args.min_size:
        try:
            min_size = int(args.min_size)
        except ValueError:
            try:
                unit = args.min_size[-1]
                min_size = int(args.min_size[0:-1]) * unit_sizes[unit.lower()]
            except (KeyError, ValueError):
                parser.error("unparseable minimum size: {}".format(args.min_size))

    files = [i for i in find_files(args.base_dir, min_size=min_size, verbose=args.verbose)]
    files.sort(key=lambda x: x[1])

    if args.limit:
        files = files[-(args.limit):]

    for item in files:
        try:
            print(args.format.format(fsize=size_to_units(item[1], args.unit, args.round), unit=unit_names[args.unit],
                                     fpath=item[0]))
        except UnicodeEncodeError:
            sys.stderr.write("Invalid UTF-8 file name: {}\n".format(repr(item[0])))
            sys.stderr.flush()
            clean = False

    if not clean:
        sys.stderr.write("Warning: errors were encountered while scanning files\n")
        sys.stderr.flush()

    return 0 if clean else 1

if __name__ == '__main__':
    sys.exit(main())
