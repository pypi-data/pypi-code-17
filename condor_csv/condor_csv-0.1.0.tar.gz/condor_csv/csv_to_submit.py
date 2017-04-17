#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create a HTCondor submit file from a CSV file.

Input is a file formatted as by Excel's CSV writing. We take this and, for
every row, write a job entry for an HTCondor submit file. Command names are
expected in the header row.

Columns with values that are the same in every row (often for universe,
executable, and getenv commands) will be written at the top before any per-job
clauses. This is only for human readability -- the submit file would work the
same either way.

The only specially-handled case is a column labeled "#skip". If this column
exists, anywhere it has a value other than blank, "0", "f, false", or "n"
the corresponding job clause will be commented out.

Documentation for submit file commands is available here:
http://research.cs.wisc.edu/htcondor/manual/current/condor_submit.html

Usage:
  condor_csv [options] <input_file>
  condor_csv -h

Options:
  -h                      Show this screen
  --version               Show version
  --output=<output_file>  Write to this file instead of standard output
  -v, --verbose           Print debugging information to standard error
"""

from __future__ import (
    absolute_import,
    print_function,
    with_statement,
    division,
    unicode_literals)

import sys
import io
import csv
import re
from contextlib import contextmanager

from condor_csv.vendor.docopt import docopt

from condor_csv import _metadata

import logging
logging.basicConfig(format='%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.WARN)

SKIP_RE = re.compile("^#skip$", re.IGNORECASE)
FALSY_RE = re.compile("(^$)|(^n$)|(^f$)|(^false$)|(^0+$)", re.IGNORECASE)


def transpose_nested(l):
    return map(list, zip(*l))


def strip_whitespace(nested_list):
    # Strip whitespace from every cell
    return [
        [val.strip() for val in row]
        for row in nested_list]


def clean_csv(csvlike):
    # Cleans a 2-d dataset. For now, this just strips whitespace
    # from every element.
    return strip_whitespace(csvlike)


def find_skip_index(headers):
    # Finds an element matching "#skip" (case insensitive)
    # raise ValueError if there's more than one.
    col = None
    for i, h in enumerate(headers):
        if SKIP_RE.match(h):
            if col:
                raise ValueError("more than one skip column found")
            col = i
    return col


def _make_skip_column(headers, data):
    # If there's a header that looks like #skip, return a boolean column
    # from data that column. Otherwise, return a column of False values
    # of the same length.
    # data must be column-wise, and the same length as headers
    # WARNING: MODIFIES headers AND data
    if not len(headers) == len(data):
        raise ValueError("headers and data are not the same length")
    skip_index = find_skip_index(headers)
    if not skip_index:
        return [False] * len(data[0])
    headers.pop(skip_index)  # Throw this away
    skip_column = data.pop(skip_index)
    matches = [FALSY_RE.match(v) for v in skip_column]
    return [not m for m in matches]


def _make_constants_varyings(headers, data):
    # Split the headers and data into constant and varying lists
    usage_counts = [len(set(col)) for col in data]
    constants = []
    varyings = []
    for count, header, data in zip(usage_counts, headers, data):
        if count == 1:
            constants.append((header, data[0]))
        elif count > 1:
            varyings.append((header, data))
        else:
            raise ValueError("data appears to be empty!")
    return constants, varyings


def make_constant_varying_skip(nested_list):
    # This turns a nested list into three things:
    # 1: A list of constants (unchanging) in (header, value) pairs
    # 2: A list of varying values (one per row) in (header, list) pairs
    # 3: A set of "skip" values (one value per row) if the list has a
    #    "#skip" column, or None otherwise.
    headers = nested_list[0][:]  # The last [:] forces a copy
    rowwise_data = nested_list[1:]
    # Flip the data so it's indexed by column first
    data = list(transpose_nested(rowwise_data))
    skip_data = _make_skip_column(headers, data)
    constants, varyings = _make_constants_varyings(headers, data)

    return constants, varyings, skip_data


def write_constants(constants, out):
    # Write the constant parts of the submit file to the submit output
    for attribute, value in constants:
        out.write("{0} = {1}\n".format(attribute, value))
    out.write("\n")


def write_varyings(varyings, skips, out):
    # Write the per-job clauses to the submit output
    for rownum, skip in enumerate(skips):
        comment = ""
        if skip:
            comment = "# "
        for attribute, column in varyings:
            out.write("{0}{1} = {2}\n".format(
                comment, attribute, column[rownum]))
        out.write("{0}Queue\n".format(comment))
        out.write("\n")


def make_submit_from_csvlike(csvlike, out):
    # Assumes csvlike is a 2-dimensional iterable.
    # 1: Partition rows into three lists, column-wise (first row is headers)
    #   - Constant columns (one value in the column)
    #   - Varying columns (more than one value in the column)
    #   - "skip" column (header is "#skip"). More than one skip column
    #     is an error.
    # 2: Write all the constant columns
    # 3: For each row in rows:
    #   1: If skip for this row is truthy, comment all following
    #   2: For each column in varying columns, write that value
    #   3: Write "Queue"
    csv_cleaned = clean_csv(csvlike)
    constants, varyings, skips = make_constant_varying_skip(csv_cleaned)
    write_constants(constants, out)
    write_varyings(varyings, skips, out)


@contextmanager
def file_or_stdout(filename=None):
    # Create an object with the same API whether it's a file or stream
    out_stream = sys.stdout
    if filename:
        out_stream = open(filename, "w")
    try:
        yield out_stream
    finally:
        if filename:
            out_stream.close()


def make_submit(argv):
    pargs = docopt(__doc__, argv, version=_metadata.__version__)
    if pargs.get('--verbose'):
        logger.setLevel(logging.DEBUG)
    logger.debug(pargs)
    with file_or_stdout(pargs.get('--output')) as out_stream:
        infile = io.open(pargs.get('<input_file>', 'rU'), encoding='utf-8-sig')
        reader = csv.reader(infile)
        make_submit_from_csvlike(reader, out_stream)


def main():
    # Parse the command line
    # Open and clean (eg, strip()) the input file
    # Open the output
    # Make the submit from the input
    argv = sys.argv[1:]
    make_submit(argv)

if __name__ == '__main__':
    main()
