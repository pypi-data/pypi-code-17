#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
sql(ite) explorer/exporter
"""

# imports
import argparse
import csv
import os
import sys
from .model import SQLEx


def ensure_dir(directory):
    """ensure a directory exists"""
    if os.path.exists(directory):
        if not os.path.isdir(directory):
            raise OSError("Not a directory: '{}'".format(directory))
        return directory
    os.makedirs(directory)
    return directory


class SQLExParser(argparse.ArgumentParser):
    """CLI option parser"""

    def __init__(self, **kwargs):
        kwargs.setdefault('formatter_class', argparse.RawTextHelpFormatter)
        kwargs.setdefault('description', __doc__)
        argparse.ArgumentParser.__init__(self, **kwargs)
        self.add_argument('db',
                          help="sqlite `.db` file")
        self.add_argument('table', nargs='?',
                          help="table to operate on")
        self.add_argument('--tables', '--list-tables', dest='list_tables',
                          action='store_true', default=False,
                          help="list tables and exit")
        self.add_argument('--columns', '--list-columns', dest='list_columns',
                          action='store_true', default=False,
                          help="list columns in `table` and exit")
        self.add_argument('-o', '--output',
                          help="output to directory (if `table` not given), or filename or stdout by default")
        self.add_argument('--header', dest='header',
                          action='store_true', default=False,
                          help="export header as first row")
        self.options = None

    def parse_args(self, *args, **kw):
        options = argparse.ArgumentParser.parse_args(self, *args, **kw)
        self.validate(options)
        self.options = options
        return options

    def validate(self, options):
        """validate options"""

        try:
            open(options.db).close()
        except Exception as e:
            self.error("Could not open '{}': {}".format(options.db, e))

        if not any((options.output,
                    options.list_tables,
                    options.table)):
            self.error("`--output` directory must be specified to output entire database")

        if options.list_columns and not options.table:
            self.error("`--list-columns` requires `table`")

def main(args=sys.argv[1:]):
    """CLI"""

    # parse command line options
    parser = SQLExParser()
    options = parser.parse_args(args)

    # connect to database
    db = SQLEx(options.db)

    if options.list_tables:
        # list tables and return
        # if `table` argument is provided, exit 1
        # if not available.  Otherwise exit 0
        tables = db.tables()
        print ('\n'.join(tables))
        retval = 0
        if options.table:
            retval = int(options.table not in tables)
        return retval

    if options.table:
        # ensure selected table exists
        if options.table not in db.tables():
            parser.error("No table '{}' in {} tables:\n{}".format(options.table, options.db, ', '.join(db.tables())))

    if options.list_columns:
        # list columns and return
        print ('\n'.join(db.columns(options.table).keys()))
        return

    if options.table:
        # output table

        if options.output:
            with open(options.output, 'w') as f:
                db.table2csv(options.table, f, header=options.header)
        else:
            db.table2csv(options.table, sys.stdout, header=options.header)
            sys.stdout.flush()
    else:
        # output entire db to CSV files in directory

        # ensure directory exists
        ensure_dir(options.output)

        for table in db.tables():
            # export each table
            path = os.path.join(options.output, '{}.csv'.format(table))
            with open(path, 'w') as f:
                db.table2csv(table, f, header=options.header)


if __name__ == '__main__':
    main()
