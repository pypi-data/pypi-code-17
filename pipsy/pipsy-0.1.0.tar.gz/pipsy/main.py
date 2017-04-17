from __future__ import absolute_import
import sys
import argparse
from urllib.error import HTTPError
import pipsy


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('packages', metavar='packages', type=str, nargs='*',
                        help='Packages to check, if not supplied, all installed packages will be checked')
    parser.add_argument('-c', '--changelog-security-check', dest='check_changelogs', action='store_true', default=False,
                        help='Check changelogs for possible security notices')
    parser.add_argument('-j', '--output-json', dest='output_json', action='store_true', default=False,
                        help='Output results as JSON')
    args = parser.parse_args()
    pipsy.show_updates(changelog_scan=args.check_changelogs,
                       json_out=args.output_json, filter_packages=args.packages)


if __name__ == '__main__':
    main()
