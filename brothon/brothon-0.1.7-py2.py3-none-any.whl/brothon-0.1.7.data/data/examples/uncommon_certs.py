"""FileTailer Python Class"""
from __future__ import print_function
import os
import sys
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

    # Sanity check that this is a x509 log
    if not args.bro_log.endswith('x509.log'):
        print('This example only works with Bro x509.log files..')
        sys.exit(1)

    # File may have a tilde in it
    if args.bro_log:
        args.bro_log = os.path.expanduser(args.bro_log)

        # Run the bro reader on a given log file counting up user agents
        cert_issuer = Counter()
        cert_subject = Counter()
        reader = bro_log_reader.BroLogReader(args.bro_log, tail=True)
        for count, row in enumerate(reader.readrows()):
            # Track counts
            cert_issuer[row['certificate.issuer']] += 1
            cert_subject[row['certificate.subject']] += 1

            # Every hundred rows report agent counts (least common)
            if count%100==0:
                print('\n<<<Least Common Cert Issuer>>>')
                pprint(cert_issuer.most_common()[:-5:-1])
                print('\n<<<Least Common Cert Subject>>>')
                pprint(cert_subject.most_common()[:-5:-1])

        # Also report at the end (if there is one)
        print('\n<<<Least Common Cert Issuer>>>')
        pprint(cert_issuer.most_common()[:-5:-1])
        print('\n<<<Least Common Cert Subject>>>')
        pprint(cert_subject.most_common()[:-5:-1])
