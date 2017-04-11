"""
Alternative monitor for PostgreSQL CSV logs. This was written against the log
format of PostgreSQL 9.1. Note that the CSV format might change across
versions, and this script might breach. However, it is easily changed!
"""
from __future__ import print_function
from argparse import ArgumentParser
from collections import namedtuple
from time import sleep
import csv
import sys

try:
    import blessings
    TERM = blessings.Terminal()
except ImportError:
    TERM = None

LogRecord = namedtuple("LogRecord",
                       'log_time,'
                       'user_name,'
                       'database_name,'
                       'process_id,'
                       'connection_from,'
                       'session_id,'
                       'session_line_num,'
                       'command_tag,'
                       'session_start_time,'
                       'virtual_transaction_id,'
                       'transaction_id,'
                       'error_severity,'
                       'sql_state_code,'
                       'message,'
                       'detail,'
                       'hint,'
                       'internal_query,'
                       'internal_query_pos,'
                       'context,'
                       'query,'
                       'query_pos,'
                       'location,'
                       'application_name')


class StreamIterator(object):
    """
    Python's default CSV reader assumes that the values don't contain
    newlines. It reads files linewise. This poses problems for PostgreSQL
    logs, if the queries contained newlines. As the log records are properly
    escaped however, we can deal with this.

    This iterator will read the files *bytewise* and emit new CSV records only
    if a newline is found which is *not* inside an escaped string value.
    """
    def __init__(self, f):
        self.f = f
        self.inside_quote = False

    def __iter__(self):
        return self

    def __next__(self):
        last_char = ''
        inside_quote = False
        char = self.f.read(1)
        output = []
        while True:
            if char == '\n' and not inside_quote:
                return ''.join(output)

            if char == '"':
                inside_quote = not inside_quote

            output.append(char)
            last_char = char
            char = self.f.read(1)

            while not char:
                # keep reading ("tail -f" like behaviour)
                sleep(0.1)
                char = self.f.read(1)


def parse_args(cmdargs):
    """
    Sets up the command-line arguments.

    Returns the parsed arguments.
    """
    parser = ArgumentParser(
        description='Monitor a PostgreSQL CSV log file.')
    parser.add_argument('-d', '--database', default='',
                        help=('Limit logs to the named database'))
    parser.add_argument('filename', nargs=1)

    args = parser.parse_args(cmdargs)
    if not args.filename:
        parser.error('You must specify a filename!')

    return args


def printout(record):
    """
    Simple handler for log records. Prints the log record to stdout
    """
    if TERM:
        if record.error_severity == 'ERROR':
            line_color = TERM.red
            message_color = TERM.yellow
        else:
            line_color = TERM.white
            message_color = TERM.green
        message = (
            '{1.bold}{2}{0.log_time} '
            '{0.user_name} '
            '{0.database_name} '
            '{0.connection_from} '
            '{0.error_severity} '
            '{0.application_name}{1.normal}\n'
            '{3}{0.message}{1.normal}'.format(
                record,
                TERM,
                line_color,
                message_color))
    else:
        message = (
            '{0.log_time} '
            '{0.user_name} '
            '{0.database_name} '
            '{0.connection_from} '
            '{0.error_severity} '
            '{0.application_name}\n'
            '{0.message}'.format(record))

    print(message)


def monitor(filename, database='', handler=printout):
    """
    Start monitoring the given filename.
    """
    with open(filename, 'r') as csvfile:
        csvfile.seek(0, 2)
        reader = csv.reader(StreamIterator(csvfile), delimiter=",", quotechar='"')
        for row in reader:
            row = LogRecord(*row)
            if not database or row.database_name == database:
                handler(row)


def main():
    if sys.version_info < (3, 3):
        print('Requires at least Python 3.3', file=sys.stderr)
        return 1
    args = parse_args(sys.argv[1:])
    if args.database:
        print('*** Only showing entries for database %s' % args.database)
    try:
        monitor(args.filename[0], args.database)
    except KeyboardInterrupt:
        print('Bye')
    return 0


if __name__ == '__main__':
    sys.exit(main())
