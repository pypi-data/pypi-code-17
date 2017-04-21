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
from .formats import camel_to_dashed, format_as_text, format_as_json
import configparser


def config_path():
    return os.path.join(os.path.expanduser('~'), '.acs', 'config.ini')


def load_profiles():
    path = config_path()
    try:
        config = configparser.ConfigParser()
        config.read_file(open(path))
        #print('Loaded profiles:', config.sections())
        return config
    except FileNotFoundError:
        sys.exit("File not found: {config} (create with configure, see 'configure --help')".format(config=path))


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
        #print("No existing config file")
        profiles = configparser.ConfigParser()

    #print('Existing sections:', profiles.sections())

    # Update the specified profile
    profiles[profile] = config
    #print('Modified sections:', profiles.sections())

    # Create parent directory, if required
    if not os.path.exists(os.path.dirname(path)):
        os.mkdir(os.path.dirname(path))

    with open(path, 'w') as config_file:
        profiles.write(config_file)


def default_command(args):
    print('Missing command. See --help for details')


def login(args):
    try:
        config = load_config(args.profile)
    except KeyError:
        sys.exit('No profile named "{profile}" exists. Have you created it with "--profile={profile} configure"?'.
                 format(profile=args.profile))
    url = args.url or config['acs_server_url']
    username = args.username or config['username']

    client = Client(url)
    if args.password:
        password = args.password
    else:
        print('Logging in {user} to {server}'.format(user=username, server=url))
        password = getpass.getpass('Password: ')
    response = client.auth.create_ticket(username, password)
    if response.status_code == 201:
        ticket = response.json()['entry']['id']

        # Only update the ticket in the config, other settings remain unchanged, even
        # if overridden, e.g. acs login --username=another
        config['ticket'] = ticket
        save_config(args.profile, config)
    else:
        print('Error during authentication: %d (%s)' % (response.status_code, response.json()['error']['briefSummary']))


def configure(args):
    url = args.url
    username = args.username

    # Profiles other than DEFAULT will inherit from the DEFAULT profile, so do not
    # need default values to be supplied by the argparse parser (this would stop the
    # inheritance from working).
    # The DEFAULT profile therefore is the only one that requires true 'default' arg values.
    if args.profile == 'DEFAULT':
        url = url or 'http://localhost:8080/alfresco'
        username = username or 'admin'

    config = dict()
    if url:
        config['acs_server_url'] = url
    if username:
        config['username'] = username

    save_config(args.profile, config)


def api_handler(args):
    try:
        config = load_config(args.profile)
    except KeyError:
        sys.exit('No profile named "{profile}" exists. Have you created one with "--profile={profile} configure"?'.
                 format(profile=args.profile))

    try:
        ticket = config['ticket']
    except KeyError:
        sys.exit('No ticket found. Have you logged in?')

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
        response = client.apis[api].create_entity(ticket, args.op_def['path'], args, args.op_def['properties'], args.op_def['optional-properties'])
    elif op.startswith('update-'):
        response = client.apis[api].update_entity(ticket, args.op_def['path'], args, args.op_def['properties'], args.op_def['optional-properties'])
    elif op.startswith('delete-'):
        response = client.apis[api].delete_entity(ticket, args.op_def['path'], args)
    elif op.startswith('upload-'):
        response = client.apis[api].upload_content(ticket, args.op_def['path'], args)
    else:
        print('API Command', args)

    # Post-process the response for 200-299 (positive HTTP responses)
    if response is not None:
        if response.status_code == 204:
            # "No content"
            response_data = None
        elif (response.status_code in range(200, 300)) and args.query:
            response_data = jmespath.search(args.query, response.json())
        else:
            response_data = response.json()

        if response_data is not None:
            if args.output == 'json':
                format_as_json(response_data, sys.stdout)
            elif args.output == 'text':
                format_as_text(response_data, sys.stdout)
            else:
                sys.exit('Output format {} not recognised.'.format(args.output))


def create_parser(apidefs):
    parser = argparse.ArgumentParser()
    parser.set_defaults(command=None, api_operation=None)

    # Global options
    parser.add_argument('--version', action='version', version='%(prog)s '+version)
    parser.add_argument('--profile', default='DEFAULT', help='name of the profile to use, e.g. my-dev-server')
    parser.set_defaults(func=default_command)

    sp = parser.add_subparsers(dest='command', title='commands', description="""
    A command may be the name of an API group (e.g. 'sites') and must be followed by a command
    name (e.g. 'create-site'), or it may be an application command such as 'login' that may or may not require
    a subcommand.
    Use '%(prog)s <command> --help' for more information about a particular command.""",
                               metavar='<command>',
                               help='may be one of the following:')

    # Common profile arguments - optional arguments used by configure and login
    common_profile_parser = argparse.ArgumentParser(add_help=False)
    common_profile_parser.add_argument('--username', help='username to use for authentication, e.g. admin')
    common_profile_parser.add_argument('--url', help='server URL, e.g. http://localhost:8080/alfresco')

    login_parser = sp.add_parser('login', description="""
    Login using the specified profile. The 'DEFAULT' profile will be used
    if the --profile option doesn't specify a profile (see 'acs --help').
    An authentication ticket will be generated and stored with the profile
    information (see the file $HOME/.acs/config.ini)
    The login password may be supplied using the --password option, or if
    not specified, the user will be interactively prompted for a password (recommended).
    """, help='login and store an authorization ticket', parents=[common_profile_parser])

    login_parser.add_argument('--password', help='authentication password', default=None)
    login_parser.set_defaults(func=login)

    config_parser = sp.add_parser('configure',
                                  help="configure a profile, the 'DEFAULT' profile if not specified",
                                  parents=[common_profile_parser])
    config_parser.set_defaults(func=configure)

    add_api_operations(sp, apidefs)

    return parser


def option_from_camel(camel_case):
    return '--'+camel_to_dashed(camel_case)


def add_json_arguments(op, optional_grp, require_grp):
    optional_grp.add_argument('--json-data', help='''
        JSON payload for the API method.
        Properties that have named options (e.g. --user-name) may alternatively be
        specified in the JSON option (e.g. userName).''')
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
    api_common_grp.add_argument('--fields', help='restrict the set of fields that will be returned')
    api_common_grp.add_argument('--include', help='include optional fields in the results')
    api_common_grp.add_argument('--where', help='"where clause" to restrict the set of results')
    api_common_grp.add_argument('--output', choices={'json', 'text'}, default='json', help='output format, default is json')

    # Arguments common to list APIs
    paged_parser = argparse.ArgumentParser(add_help=False)
    paged_grp = paged_parser.add_argument_group(title='options relating to pageable API calls')
    paged_grp.add_argument('--max-items', type=int, help='Maximum number of items to return')
    paged_grp.add_argument('--skip-count', type=int, help='Number of items to skip before including results')
    
    for api_name, api in apidefs.items():
        api_parser = subparsers.add_parser(api_name, help='the {0} API (see "%(prog)s {0} --help")'.format(api_name))
        api_parser.set_defaults(func=api_handler)
        api_subparsers = api_parser.add_subparsers(title='API command (required)', metavar='<command>', help='may be one of the following:', description="use '%(prog)s <command> --help' for further information".format(api=api_name), dest='api_operation')
        for op_name, op in api['operations'].items():
            op_parser = None
            if op_name.startswith('get-'):
                op_parser = api_subparsers.add_parser(op_name, parents=[api_common_parser], help='get an entity by ID')
            elif op_name.startswith('list-'):
                op_parser = api_subparsers.add_parser(op_name, parents=[api_common_parser, paged_parser], help='list items')
            elif op_name.startswith('create-'):
                op_parser = api_subparsers.add_parser(op_name, parents=[api_common_parser], help='create an entity')
                api_required_props_grp = op_parser.add_argument_group(title='required creation properties')
                api_optional_props_grp = op_parser.add_argument_group(title='optional creation properties')
                add_json_arguments(op, api_optional_props_grp, api_required_props_grp)
                # TODO: refactor, refactor, refactor...
                for file_param in op.get('files', []):
                    op_parser.add_argument(option_from_camel(file_param), dest=file_param, required=False,
                                           type=argparse.FileType('rb'),
                                           help='specifies a file to upload'.format(file_param))
            elif op_name.startswith('update-'):
                op_parser = api_subparsers.add_parser(op_name, parents=[api_common_parser], help='update an entity')
                api_optional_props_grp = op_parser.add_argument_group(title='optional update properties')
                api_required_props_grp = op_parser.add_argument_group(title='required update properties')
                add_json_arguments(op, api_optional_props_grp, api_required_props_grp)
            elif op_name.startswith('delete-'):
                op_parser = api_subparsers.add_parser(op_name, parents=[api_common_parser], help='delete an entity by ID')
            elif op_name.startswith('upload-'):
                op_parser = api_subparsers.add_parser(op_name, parents=[api_common_parser], help='upload content for an entity')
                for file_param in op['files']:
                    op_parser.add_argument(option_from_camel(file_param), dest=file_param, required=True,
                                           type=argparse.FileType('rb'),
                                           help='specifies a file to upload'.format(file_param))
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


