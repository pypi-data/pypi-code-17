'''
Command line functionality
'''
import argparse

import vagrepo.repository

_PARSER = argparse.ArgumentParser()
_PARSER.add_argument('--path', dest='path')

_SUBPARSERS = _PARSER.add_subparsers(dest='subcommand')
_SUBPARSERS.add_parser('list', help='list available boxes')
_CREATE_PARSER = _SUBPARSERS.add_parser('create', help='create new empty box')
_CREATE_PARSER.add_argument('name', metavar='NAME')
_CREATE_PARSER.add_argument('--description')

def parse_args():
    '''Create configured parser instance'''
    return _PARSER.parse_args()

def print_help():
    '''Print command line help message'''
    _PARSER.print_help()

def handle(namespace):
    '''
    handle parsed command line arguments, route call to correct subcommand
    handler function
    '''
    if namespace.subcommand is None:
        print_help()
    elif namespace.subcommand == 'list':
        repository = vagrepo.repository.Repository(namespace.path)
        handle_list(namespace, repository)
    elif namespace.subcommand == 'create':
        repository = vagrepo.repository.Repository(namespace.path)
        handle_create(namespace, repository)

def handle_list(_, repository):
    '''handle list subcommand'''
    for name in repository.box_names:
        print(name)

def handle_create(namespace, repository):
    '''handle create subcommand'''
    repository.create(namespace.name, namespace.description)
