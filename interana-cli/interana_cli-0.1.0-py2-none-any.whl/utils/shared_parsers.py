# Copyright 2017 Interana, Inc.
from interana._version import __version__

def add_verbose_errors(p):
    '''Add verbose error logging (stacktraces)

    Almost every command should use this.
    '''
    p.add_argument(
        '-v',
        '--verbose',
        help='More output e.g. stacktraces on errors',
        action='store_true'
    )


def add_output_parameters(p):
    '''Add output option

    Any command that can generate/display output should probably use this
    '''
    p.add_argument(
        '--output',
        help='Set output format. Default is "table"',
        choices=['json', 'text', 'table'],
        default='table',
        type=str
    )


def add_credential_handle(p):
    '''Allow a command to be run against the non-default instance

    Almost every command should use this.
    '''
    p.add_argument(
        '--instance-name',
        metavar='handle',
        help='Use specific stored credential instead of default',
        default='default'
    )


def add_clowntown_ssl(p):
    '''Allow commands to skip SSL certificat verification'''
    p.add_argument(
        '--unsafe',
        dest='clowntown',
        help='Do not verify SSL certs. DEV ONLY! DANGER!',
        action='store_true'
    )


def add_run_mode(p):
    '''Adds run mode for modules that defaults to dry-run (most deletes on data).'''
    p.add_argument(
        '--run',
        '-r',
        help='Use to execute command (dry run is default).',
        action='store_const',
        const=1,
        default=0,
    )


def add_version(p):
    '''Adds version flag to display CLI version, i.e. ia 0.1.0'''
    p.add_argument(
        '--version',
        action='version',
        version='%(prog)s {version}'.format(version=__version__)
    )
