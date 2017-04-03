# Copyright 2017 Interana, Inc.
from collections import OrderedDict, namedtuple
import argparse
import json
import os
import requests

from interana.utils import config
from interana.utils.shared_parsers import (add_clowntown_ssl, add_verbose_errors, add_credential_handle, add_version)


clowntown = '''
NOW ENTERING...
   ___  __     __   _  _  __ _  ____  __   _  _  __ _
  / __)(  )   /  \ / )( \(  ( \(_  _)/  \ / )( \(  ( \\
 ( (__ / (_/\(  O )\ /\ //    /  )( (  O )\ /\ //    /
  \___)\____/ \__/ (_/\_)\_)__) (__) \__/ (_/\_)\_)__)

YOU HAVE NO SSL VERIFICATION, YOU COULD BE TALKING TO ANYONE
'''


class DoResult(object):
    ''' All do() implementations should return a DoResult
        entries - a list of list of values
        headers - a list of strings. The headers correspond to the lists in `entries` by index
        message - text to show in the end of the formatted table
        empty_warning - text to show when no applicable results were found'''

    def __init__(self, entries=None, headers=None, message=None, empty_warning=None):
        self.entries = entries
        self.headers = headers
        self.message = message
        if empty_warning:
            self.empty_warning = empty_warning
        else:
            self.empty_warning = "No results found. Please check your input."


class _CommandBase(object):

    def __init__(self):
        self.hostname = ''
        self.api_token = ''

    def parser_setup(self, sps):
        '''override this in your child class to set up CLI args to your liking'''

        # use this line first
        # parser = self.init_parser(sps)
        raise NotImplementedError("Not implemented yet")

    def initialize(self, args):
        self.args = args
        self.args_dict = vars(args)

        # provided by add_credential_handle
        self.instance_name = self.args_dict.get('instance_name', 'default')

        # provided by add_clowntown_ssl
        default = os.environ.get('CLOWNTOWN')
        self.clowntown = self.args_dict.get('clowntown') or default
        if self.clowntown:
            if self.clowntown != 'ultraclown':
                print clowntown
            requests.packages.urllib3.disable_warnings()

        return self

    def do(self):
        '''put the actual implementation of the command here'''
        raise NotImplementedError("Not implementated yet")

    def _handle_basic_response(self, res):
        '''
        For a lot of query API endpoints, the return value is a JSON dict with "msg" and "success"
        '''
        content = json.loads(res.content)
        return DoResult(message=content['msg'])

    def _handle_no_msg_response(self, res, success_msg, failure_msg):
        '''
        Some endpoints do not return a message, so this is a convenience method to print a message to the user
        after receiving a response with no message
        '''
        content = json.loads(res.content)
        if content.get('success'):
            msg = success_msg
        else:
            msg = failure_msg
        return DoResult(message=msg)

    def _prepare_kwargs(self, authenticated, kwargs):

        if authenticated:
            try:
                rc_config = config.get_credentials(self.instance_name)
                self.hostname = rc_config['hostname']
                self.api_token = rc_config['api_token']
                self.customer_id = rc_config.get('customer_id')
            except:
                raise Exception("Could not read credentials from .interanarc: Did you forget to run config?")

            headers = kwargs.pop('headers', {})
            headers['Authorization'] = 'Token ' + self.api_token
            if self.customer_id:
                headers['X-Service-As-Customer-Id'] = str(self.customer_id)
            kwargs['headers'] = headers

        kwargs['verify'] = not self.clowntown

    def _ok(self, res):
        code = res.status_code
        if code == 401:
            raise Exception("Bad credentials, Authentication failed, try re-running config")
        if code == 403:
            raise Exception("Unauthorized. Check user's roles")
        if code != 200:
            default_msg = 'Received unexpected error code {} from server.'.format(code)
            try:
                content = json.loads(res.content)
                error_keys = ['error', 'exception', 'msg']
                error_msg = next((content.get(k) for k in error_keys if k in content), default_msg)
            except ValueError:
                # sometimes there is no json-parseable error message from server.
                error_msg = default_msg
            raise Exception(error_msg)
        return res

    def get(self, url, authenticated=True, params=None, **kwargs):
        self._prepare_kwargs(authenticated, kwargs)
        return self._ok(
            requests.get(url.format(hostname=self.hostname),
                         params=params,
                         **kwargs))

    def post(self, url, authenticated=True, params=None, **kwargs):
        self._prepare_kwargs(authenticated, kwargs)
        return self._ok(
            requests.post(url.format(hostname=self.hostname),
                          params=params,
                          **kwargs))

    def post_json(self, url, authenticated=True, params=None, **kwargs):
        if 'data' in kwargs:
            kwargs['data'] = json.dumps(kwargs['data'])
        return self.post(url, authenticated=authenticated, params=params, **kwargs)


class CommandHandler(_CommandBase):

    name = None         # name of subcommand for CLI
    description = None  # help string for command

    def __init__(self):
        super(CommandHandler, self).__init__()
        self.subcommands = OrderedDict()

    def register_subcommand(self, subcommand):
        name = subcommand.name
        self.subcommands[name] = subcommand

    def parser_setup(self, sps):
        parser = sps.add_parser(self.name, help=self.description)
        parser.set_defaults(command=self.name)
        add_version(parser)

        if self.subcommands:
            # add a help if there are subcommands
            self.subcommands['help'] = HelpSubHandler(parser)
            sub_sps = parser.add_subparsers()
            for _, sub in self.subcommands.iteritems():
                sub.parser_setup(sub_sps)

        return parser


class SubCommandHandler(_CommandBase):

    name = None         # name of subcommand for CLI
    description = None  # help string for command

    def init_parser(self, sps, **kwargs):
        '''
        This is a simple boilerplate helper, Every subcommand should call this as
        the first line of parser_setup unless you have a very good reason
        otherwise
        '''
        parser = sps.add_parser(
            self.name,
            formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50),
            help=self.description,
            **kwargs)
        parser.set_defaults(subcommand=self.name)

        g = parser.add_argument_group("Generic")
        add_verbose_errors(g)
        add_clowntown_ssl(g)
        add_credential_handle(g)
        add_version(g)

        return parser


# special classes to implement help verb
class HelpHandler(CommandHandler):
    name = 'help'
    description = 'Prints help. ^_^'

    def __init__(self, parent_parser):
        ''' Takes the parent_parser to print out help when called. '''
        self.parent_parser = parent_parser

    def parser_setup(self, sps):
        parser = sps.add_parser(self.name, help=self.description)
        parser.set_defaults(command=self.name)

    def do(self):
        self.parent_parser.print_help()


class HelpSubHandler(SubCommandHandler):
    name = 'help'
    description = 'Prints help. ^_^'

    def __init__(self, parent_parser):
        ''' Takes the parent_parser to print out help when called. '''
        self.parent_parser = parent_parser

    def parser_setup(self, sps):
        self.init_parser(sps)

    def do(self):
        self.parent_parser.print_help()


def _pretty_print_dict(value):
    output = ''
    for k, v in value.iteritems():
        output += '{}: {}\t'.format(k, v)
    return output
