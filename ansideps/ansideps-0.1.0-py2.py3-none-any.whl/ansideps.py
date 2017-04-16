#!/usr/bin/env python

from __future__ import print_function
import logging
import os
import re
import sys

import click
import networkx as nx
import yaml


try:
    import pydotplus
    HAS_DOT = True
except ImportError:
    HAS_DOT = False

__version__ = "0.1.0"
__author__ = "Duncan Hutty"
__license__ = "MIT"

LOG_LEVELS = ['ERROR', 'WARNING', 'INFO', 'DEBUG']
ANSIBLE_ROLES_PATH = getattr(os.environ, 'ANSIBLE_ROLES_PATH', './test_roles')
logger = logging.getLogger(__name__)


def _open_yaml_file(filename):
    """Read a file that contains yaml, return it as a dict."""
    try:
        with open(filename, 'r') as yaml_stream:
            return yaml.load(yaml_stream)
    except IOError:
        return None


def _get_roles(roles_path, exclude_pattern=None):
    """Return a filtered list of roles from the roles_path's directories."""
    roles = os.listdir(roles_path)
    if exclude_pattern is not None:
        for role in roles:
            if exclude_pattern.search(role):
                logger.info('Excluding {}'.format(role))
                roles.remove(role)
    return roles


def _build_graph(dg, path, roles):
    """Return a directed graph where each node is a role and each edge is a dependency relationship."""
    for role in roles:
        dg.add_node(role)
        md = _open_yaml_file(os.path.join(path, role, 'meta', 'main.yml'))
        if md is None:
            logger.warning('{} has no meta/main.yml'.format(role))
        else:
            deps = md.get('dependencies')
            logger.debug('{} has deps {}'.format(role, deps))
            for dep in deps:
                dg.add_edge(role, dep)
    return dg


@click.command(
    'resolve', short_help="Resolve Ansible role dependency relationships")
@click.argument('role', nargs=-1)
@click.option(
    '--roles-path',
    default=ANSIBLE_ROLES_PATH,
    show_default=True,
    help='Colon-delimited search path for Ansible role directories')
@click.option(
    '--reverse/--no-reverse',
    default=False,
    show_default=True,
    help='return what role(s) depend on your role(s). Ancestors, not Descendants'
)
@click.option('--dotfile', help='filename for dot file')
@click.option(
    '-x',
    '--exclude-regex',
    help='Regular expression for directories to exclude')
@click.option(
    '-l',
    '--log-level',
    default='ERROR',
    show_default=True,
    type=click.Choice(LOG_LEVELS),
    help='Specify log verbosity.')
def main(role, roles_path, dotfile, exclude_regex, reverse, log_level):
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %I:%M:%S')
    if exclude_regex is not None:
        exclude_pattern = re.compile(exclude_regex)
    else:
        exclude_pattern = None
    roles = _get_roles(roles_path, exclude_pattern)
    dg = _build_graph(nx.DiGraph(), roles_path, roles)

    if dotfile:
        if HAS_DOT:
            logger.info('Writing graph to {}'.format(dotfile))
            nx.drawing.nx_pydot.write_dot(dg, dotfile)
        else:
            logger.error('Need graphviz or pydotplus to write a dotfile')
    if len(role) < 1:
        role = dg.nodes()
    role = sorted(role)
    for r in role:
        if reverse:
            for ancestor in nx.ancestors(dg, r):
                print(ancestor)
        else:
            for descendant in nx.descendants(dg, r):
                print(descendant)


if __name__ == '__main__':
    sys.exit(main())
