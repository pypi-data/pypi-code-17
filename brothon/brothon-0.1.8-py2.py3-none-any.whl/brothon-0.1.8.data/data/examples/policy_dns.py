"""Risky DNS BroThon Example"""
from __future__ import print_function
import os
import sys
import json
import argparse
from pprint import pprint

# Third Party Imports
try:
    import tldextract
except ImportError:
    print('\nThis example needs tldextract. Please do a $pip install tldextract and rerun this example')
    sys.exit(1)

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

        # Grab our 'out of policy' terms
        with open('adult_terms.json') as fp:
            terms = json.load(fp)

        # Run the bro reader on the dns.log file looking for risky TLDs
        reader = bro_log_reader.BroLogReader(args.bro_log, tail=True)
        for row in reader.readrows():

            # Pull out the domain and subdomain
            query = row['query']
            full_domain = tldextract.extract(query)
            subdomain = full_domain.subdomain
            domain = full_domain.domain

            # Check if either is 'out of policy'
            if any(term in subdomain for term in terms) or any(term in domain for term in terms):
                print('\n<<< Out of Policy DNS Found >>>')
                print('{:s} From: {:s} To: {:s}'.format(row['query'], row['id.orig_h'], row['id.resp_h']))
