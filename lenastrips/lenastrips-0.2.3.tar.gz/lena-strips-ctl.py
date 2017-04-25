#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import argparse
import logging

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

import lenastrips
from lenastrips.lenastrips import LenaPowerstrip, LenaPowerstripRequestException

if __name__ == '__main__':
    log = logging.getLogger(os.path.basename(__file__))
    auth = ('admin', 'anel')
    port = 80

    parser = argparse.ArgumentParser(description='lenastrips CLI {!s}'.format(
        lenastrips.__version__))

    parser.add_argument(
        '--dry-run', '-n',
        default=False, help='Dry Run',
        action='store_true', dest="dry_run")

    parser.add_argument(
        '--privacy',
        default=False, help='Privacy Mode: Hide MAC and IP addresses',
        action='store_true', dest="privacy")

    parser.add_argument('-v', action='count', default=0, help="verbosity",
                        dest="verbose")


    agroup = parser.add_argument_group('Authentication')
    agroup.add_argument(
        '--username', '-u',
        default=auth[0], help='Username, default: %(default)s',
        dest="username")

    agroup.add_argument(
        '--password', '-p',
        default=auth[1], help='Password, default: %(default)s',
        dest="password")

    parser.add_argument(
        '--port',
        default=port, help='Port, default: %(default)s',
        type=int, dest="port")

    groupA = parser.add_argument_group('Actions')
    groupA.add_argument(
        '--device-status', '-d',
        help='Dump device status',
        const="device_status", default=[], action='append_const', dest="actions")

    parser.add_argument("hostname")

    args = parser.parse_args()
    EOS = LenaPowerstrip(hostname=args.hostname, auth=(args.username, args.password), args=args)

    try:
        rc = EOS.main()
    except LenaPowerstripRequestException, lexc:
        log.error(lexc)
        rc = 100
    except ValueError, vexc:
        log.error(vexc)
        rc = 200

    sys.exit(rc)