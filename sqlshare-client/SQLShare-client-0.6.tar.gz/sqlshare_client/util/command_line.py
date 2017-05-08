import argparse
import re
import os
import sys


def get_oauth_values(parser=None):
    if not parser:
        parser = argparse.ArgumentParser()

    parser.add_argument('--credentials', required=False,
                        help="Path to file containing oauth credentials")

    values = vars(parser.parse_args())

    credentials_path = values["credentials"]

    if not credentials_path:
        filename = "~/.sqlshare-rest-credentials.conf"
        credentials_path = os.path.expanduser(filename)

    try:
        data = {}
        with open(credentials_path) as config_file:
            for line in config_file:
                if re.match('^#', line):
                    continue

                matches = re.match('(.*?)\s*:\s*(.*)\n*', line)
                if matches:
                    key, value = matches.groups()
                    data[key] = value
    except IOError:
        url = ("https://github.com/uw-it-aca/sqlshare-client/"
               "wiki/Command-Line-Tools")
        print "No credentials file.  Please see %s" % url
        sys.exit(2)

    keys = data.keys()
    for key in keys:
        data[key.lower()] = data[key]

    data['id'] = data['oauth_id']
    data['secret'] = data['oauth_secret']

    return data
