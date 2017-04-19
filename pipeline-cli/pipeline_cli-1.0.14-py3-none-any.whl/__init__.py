#!/usr/bin/env python

'''
    Copyright 2016 (c) Sepior Aps, all rights reserved.
'''


import os
import argparse
import json
import requests

from .__about__ import __version__


PASSWORD = os.getenv('PIPELINE_PASSWORD')
USERNAME = os.getenv('PIPELINE_USERNAME')


def authenticate(server_url):

    '''
        Authenticate towards the pipeline server.
    '''

    if not PASSWORD:
        raise Exception('PIPELINE_PASSWORD is not defined. Did you forget it?')
    if not USERNAME:
        raise Exception('PIPELINE_USERNAME is not defined. Did you forget it?')
    url = '{}/login'.format(server_url)
    headers = {'content-type': 'application/json'}
    data = json.dumps({'username': USERNAME,
                       'password': PASSWORD})
    request = requests.post(url,
                            data=data,
                            headers=headers)
    if request.status_code == 200:
        return request.json()['access_token']
    else:
        raise Exception('Authentication failed {}'.format(server_url))


def post(server_url, url, data=None, headers=None):

    '''
        Authenticate and post data to pipeline server.
    '''

    access_token = authenticate(server_url)
    if not headers:
        headers = {}
    headers['Authorization'] = access_token
    return requests.post(server_url + url, headers=headers, data=data)


def enqueue(arguments):

    '''
        Enqueue downstream pipelines wrt.
        the pipeline with pipeline_id.
    '''

    try:
        server_url = arguments.host_name
        url = '/r/pipeline/instance/{}/run-downstream/'
        url = url.format(arguments.pipeline_id)
        headers = {'content-type': 'application/json'}
        request = post(server_url, url, headers=headers)
        json_response = request.json()
        if not (request.status_code == 200 or request.status_code == 202):
            print('Could not enqueue downstream pipelines')
            print(json_response)
            exit(5)
        print(json_response)
        print('Downstream pipelines enqueued')
    except IOError as msg:
        print(str(msg))


def start(arguments):

    '''
        Start pipeline with version and pipeline
        definition file.
    '''

    try:
        with arguments.pipeline_file as file:
            data = file.read()
            server_url = arguments.host_name
            version = arguments.version
            commit_sha = arguments.commit_sha
            repository = arguments.repository
            pipeline_does_build = arguments.pipeline_does_build
            url = '/r/component/yaml/{}/{}'
            url = url.format(
                version,
                str(pipeline_does_build))
            if commit_sha and repository:
                url += '/commit/{}/{}'.format(
                    str(commit_sha),
                    str(repository))
            headers = {'content-type': 'application/json'}
            response = post(server_url, url, data=data, headers=headers)
            if not (response.status_code == 200 or
                    response.status_code == 202):
                print('Could not start pipeline')
                print(response.text)
                exit(5)
            try:
                json_response = response.json()
            except ValueError as ex:
                print(ex)
                exit(6)
            # print(json)
            if json_response['new']:
                print('Pipeline started')
            else:
                print('Pipeline already exists')
            if json_response['pipelines']:
                location = json_response['pipelines'][0]['location']
                print('See: {}{}'.format(server_url, location))
    except IOError as msg:
        print(str(msg))


def main():

    '''
        Parse command line arguments and perform the
        corresponding action.
    '''

    # Argument parser.
    # Main parser.
    parser = argparse.ArgumentParser(description='The pipeline utility')
    parser.add_argument('--version',
                        '-v',
                        action='version',
                        version='%(prog)s ' + __version__)
    parser.add_argument('--host', action="store",
                        default='https://pipeline.sepior.net',
                        dest="host_name",
                        help='specify pipeline server host. Default is https://pipeline.sepior.net')

    # Parsers for subcommands.
    subparsers = parser.add_subparsers(help='sub-commands')

    # Parser for start command.
    parser_start = subparsers.add_parser('start', help='start help')
    parser_start.add_argument('version',
                              action="store",
                              help='run pipeline with version number')
    parser_start.add_argument('--commit-sha',
                              action="store",
                              default="",
                              help='The latest commit SHA')
    parser_start.add_argument('--repository',
                              action="store",
                              default="",
                              help='The name of the Github repository')
    parser_start.add_argument('-p',
                              metavar='pipeline_file',
                              dest='pipeline_file',
                              default='pipeline.yml',
                              type=argparse.FileType('rb'),
                              help='specify pipeline file. Default is pipeline.yml')
    build_parser = parser_start.add_mutually_exclusive_group(required=False)
    build_parser.add_argument('--build',
                              dest='pipeline_does_build',
                              default=False,
                              action='store_true',
                              help='The pipeline builds artifacts as part of pipeline')
    build_parser.add_argument('--no-build',
                              dest='pipeline_does_build',
                              action='store_false',
                              help='The pipeline does not builds artifacts as part of pipeline')
    parser_start.set_defaults(command=start)

    # Parser for enqueue command.
    parser_enqueue = subparsers.add_parser('enqueue', help='enqueue downstream dependencies help')
    parser_enqueue.add_argument('pipeline_id',
                                action="store",
                                help='pipeline_id')
    parser_enqueue.set_defaults(command=enqueue)

    args = parser.parse_args()
    if 'command' in args:
        args.command(args)
    else:
        parser.print_help()
