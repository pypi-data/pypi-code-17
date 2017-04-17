# -*- coding: utf-8 -*-

"""Deploy a Takumi app.

Usage:
    takumi deploy <target> [options] [(-- <ansible_args>...)]
    takumi deploy -- <ansible_args>...
    takumi deploy -h | --help

Options:
    -t, --tags TAGS  Only run tasks with these tags
    -p, --play PLAY  Specify a different playbook
    -h, --help       Show this message and exit

Example:

    Simple deploy:

        takumi deploy testing

    Deploy a subject:

        takumi deploy testing -t cron

    Specify other playbooks:

        takumi deploy testing -p system.yml
"""

import schema
from ._base import parse_args


def run(args):
    args = parse_args('deploy', __doc__, args, {
        '--tags': schema.Or(None, str),
        '--play': schema.Or(None, str),
        '<target>': schema.Or(None, lambda x: x != '--',
                              error='Invalid value of target'),
        '<ansible_args>': list
    })

    from ..deploy import start

    try:
        start(args)
    except Exception as e:
        exit('Fail to deploy: {}'.format(e))
