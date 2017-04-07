#!/usr/bin/env python3

import argparse
from .api_defs import apis
from .common import version
import re
import os
import json
from acscli.client import Client
import jmespath
import getpass
import sys
import argcomplete
from .conventions import camel_to_dashed

def config_path():
    return os.path.join(os.path.expanduser('~'), '.acs', 'config.json')


def load_profiles():
    path = config_path()
    try:
        with open(path, 'r') as config_file:
            try:
                return json.load(config_file)
            except ValueError:
                # Invalid or missing json in the file.
                return dict()
    except FileNotFoundError:
        sys.exit("File not found: {config} (created during successful login, see 'login --help')".format(config=path))


def load_config(profile_name):
    #print('Loading profile:', profile_name)
    profiles = load_profiles()
    config = profiles[profile_name]
    #print('Loaded config: {0}'.format(config))
    return config


def save_config(profile, config):
    #print('Saving profile:', profile)
    path = config_path()
    if os.path.exists(path):
        profiles = load_profiles()
    else:
        profiles = dict()

    if not os.path.exists(os.path.dirname(path)):
        os.mkdir(os.path.dirname(path))

    with open(path, 'w') as config_file:
        # Update the specified profile
        profiles[profile] = config
        json.dump(profiles, config_file, sort_keys=True, indent=4)


def default_command(args):
    print('Missing command. See --help for details')


def login(args):
    client = Client(args.url)
    if args.password:
        password = args.password
    else:
        print('Logging in {user} to {server}'.format(user=args.username, server=args.url))
        password = getpass.getpass('Password: ')
    response = client.auth.create_ticket(args.username, password)
    if response.status_code == 201:
        ticket = response.json()['entry']['id']
        #print('Ticket: %s' % (ticket,))
        config = {
            'ticket': ticket,
            'acs_server_url': args.url
        }
        save_config(args.profile, config)
    else:
        print('Error during authentication: %d (%s)' % (response.status_code, response.json()['error']['briefSummary']))


def configure(args):
    print('Configure', args)


def api_handler(args):
    try:
        config = load_config(args.profile)
    except KeyError:
        sys.exit('No profile named "{profile}" exists. Have you logged in with "--profile={profile}"?'.
                 format(profile=args.profile))

    ticket = config['ticket']
    url = config['acs_server_url']
    client = Client(url)
    api = args.command
    op = args.api_operation
    response = None

    if op.startswith('get-'):
        response = client.apis[api].single_entity(ticket, args.op_def['path'], args)
    elif op.startswith('list-'):
        response = client.apis[api].list_collection(ticket, args.op_def['path'], args, args.skip_count, args.max_items)
    elif op.startswith('create-'):
        response = client.apis[api].create_entity(ticket, args.op_def['path'], args, args.op_def['properties'])
    elif op.startswith('update-'):
        response = client.apis[api].update_entity(ticket, args.op_def['path'], args, args.op_def['properties'], args.op_def['optional-properties'])
    elif op.startswith('delete-'):
        response = client.apis[api].delete_entity(ticket, args.op_def['path'], args)
    else:
        print('API Command', args)

    # Post-process the response for 200-299 (positive HTTP responses)
    if response is not None:
        if response.status_code == 204:
            # "No content"
            response_json = None
        elif (response.status_code in range(200, 300)) and args.query:
            response_json = jmespath.search(args.query, response.json())
        else:
            response_json = response.json()

        if response_json is not None:
            # Strip off top-level list or entry container
            # Why wouldn't it be a dict you ask? The JMESPath query *may* result
            # in a different type, for example list.pagination.count will
            # result in an int
            #if type(response_json) is dict:
            #   if 'list' in response_json:
            #        response_json = response_json['list']
            #    elif 'entry' in response_json:
            #        response_json = response_json['entry']

            print(json.dumps(response_json, indent=4))


def create_parser(apidefs):
    parser = argparse.ArgumentParser()
    parser.set_defaults(command=None, api_operation=None)

    # Global options
    parser.add_argument('--version', action='version', version='%(prog)s '+version)
    parser.add_argument('--profile', default='default', help='name of the profile to use, e.g. my-dev-server')
    parser.set_defaults(func=default_command)

    sp = parser.add_subparsers(dest='command', title='subcommands', description="""
    Use one of the following commands or APIs.
    Type '%(prog)s <command or api> --help' for more information about that specific command""", help='available commands')

    login_parser = sp.add_parser('login', help='login and store an authorization ticket')
    login_parser.add_argument('--username', default='admin')
    login_parser.add_argument('--password', default=None)
    login_parser.add_argument('--url', default='http://localhost:8080/alfresco', help='server URL, e.g. http://localhost:8080/alfresco')
    login_parser.set_defaults(func=login)

    #config_parser = sp.add_parser('configure', help='configure the tool')
    #config_parser.set_defaults(func=configure)

    add_api_operations(sp, apidefs)

    return parser


def option_from_camel(camel_case):
    return '--'+camel_to_dashed(camel_case)


def add_json_arguments(op, optional_grp, require_grp):
    optional_grp.add_argument('--json-data', help='''JSON payload for the API method.
Properties that have named options below may alternatively be specified in the JSON option.''')
    all_props = [(p, True) for p in op.get('properties', list())]
    all_props.extend([(p, False) for p in op.get('optional-properties', list())])

    for prop, isrequired in all_props:
        if isrequired:
            arg_grp = require_grp
        else:
            arg_grp = optional_grp
        # Note that they are all being flagged as NOT required, since a user can specify a property
        # in a named argument (e.g. --user-name) or as JSON (--json-data='{"userName":"..."}')
        # whether the property is REQUIRED or not affects subsequent validation of the JSON
        # (built from both sources) that will be sent during the API request.
        arg_grp.add_argument(option_from_camel(prop), dest=prop, required=False, help='{} property'.format(prop))


def add_api_operations(subparsers, apidefs):
    # options common to all API commands
    api_common_parser = argparse.ArgumentParser(add_help=False)
    api_common_grp = api_common_parser.add_argument_group(title='common API options')
    api_common_grp.add_argument('--query', help='JMESPath query')

    # Arguments common to list APIs
    paged_parser = argparse.ArgumentParser(add_help=False)
    paged_grp = paged_parser.add_argument_group(title='options relating to pageable API calls')
    paged_grp.add_argument('--max-items', type=int, help='Maximum number of items to return')
    paged_grp.add_argument('--skip-count', type=int, help='Number of items to skip before including results')
    
    for api_name, api in apidefs.items():
        api_parser = subparsers.add_parser(api_name, help='the {0} API (use "{0} --help" for more information)'.format(api_name))
        api_parser.set_defaults(func=api_handler)
        api_subparsers = api_parser.add_subparsers(title='API command (required)', description="use '%(prog)s <command> --help' for further information".format(api=api_name), dest='api_operation')
        for op_name, op in api['operations'].items():
            op_parser = None
            if op_name.startswith('get-'):
                op_parser = api_subparsers.add_parser(op_name, parents=[api_common_parser], help='get an entity by ID')
            elif op_name.startswith('list-'):
                op_parser = api_subparsers.add_parser(op_name, parents=[api_common_parser, paged_parser], help='list items')
            elif op_name.startswith('create-'):
                op_parser = api_subparsers.add_parser(op_name, parents=[api_common_parser], help='create an entity')
                api_optional_props_grp = op_parser.add_argument_group(title='optional creation properties')
                api_required_props_grp = op_parser.add_argument_group(title='required creation properties')
                add_json_arguments(op, api_optional_props_grp, api_required_props_grp)
            elif op_name.startswith('update-'):
                op_parser = api_subparsers.add_parser(op_name, parents=[api_common_parser], help='update an entity')
                api_optional_props_grp = op_parser.add_argument_group(title='optional update properties')
                api_required_props_grp = op_parser.add_argument_group(title='required update properties')
                add_json_arguments(op, api_optional_props_grp, api_required_props_grp)
            elif op_name.startswith('delete-'):
                op_parser = api_subparsers.add_parser(op_name, parents=[api_common_parser], help='delete an entity by ID')
            op_parser.set_defaults(op_def=op)
            op_path = op['path']
            required_params = re.findall('{(\w+)}', op_path)
            if op_parser:
                required_args_grp = op_parser.add_argument_group(title="required API arguments")
                for param in required_params:
                    required_args_grp.add_argument(option_from_camel(param), dest=param, required=True, help='{} parameter'.format(param))


def main():
    parser = create_parser(apis)
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()


