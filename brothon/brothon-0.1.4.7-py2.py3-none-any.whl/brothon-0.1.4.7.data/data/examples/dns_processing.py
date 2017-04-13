"""FileTailer Python Class"""
from __future__ import print_function
import os
import sys
import time
import argparse
from collections import Counter
from pprint import pprint

# Local imports
from brothon import bro_log_reader

if __name__ == '__main__':
    # Example to run the bro log reader on a given file

    # Collect args from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--bro-log', type=str, help='Specify a bro log to run BroLogReader test on')
    args, commands = parser.parse_known_args()

    # Check for unknown args
    if commands:
        print('Unrecognized args: %s' % commands)
        sys.exit(1)

    # If no args just call help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # Sanity check that this is a dns log
    if not args.bro_log.endswith('dns.log'):
        print('This example only works with Bro dns.log files..')
        sys.exit(1)

    # File may have a tilde in it
    if args.bro_log:
        args.bro_log = os.path.expanduser(args.bro_log)

        # Run the bro reader on a given log file counting up user agents
        dns_queries = Counter()
        reader = bro_log_reader.BroLogReader(args.bro_log, tail=True)
        for count, row in enumerate(reader.readrows()):
            # Skip anything with local in it
            if 'local' in row['query']:
                continue
            # Track count
            dns_queries[row['query']] += 1

            # Every 5 seconds report agent counts (least common)
            if count%100==0:
                print('\n<<<Least Common DNS Queries>>>')
                pprint(dns_queries.most_common()[:-50:-1])

        # Also report at the end (if there is one)
        print('\nLeast Common DNS Queries:')
        pprint(dns_queries.most_common()[:-50:-1])
