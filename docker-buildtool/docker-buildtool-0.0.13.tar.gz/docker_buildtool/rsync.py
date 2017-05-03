from urllib.parse import urlparse
import fnmatch
import logging
import os
from typing import List, Tuple

from docker_buildtool import utils

logger = logging.getLogger(__name__)

INCLUDE_PATH = '/tmp/include'

def parse_ignore_rules(file_lines: List[str]):
    # Filter out comments and empty lines, parse bangs.
    # Do the splitting now to make computation faster.
    rules = [(x.strip().startswith('!'), x.strip().lstrip('!').split('/')) for x in file_lines
             if x and not x.startswith('#')]
    # Try to preserve .dockerignore and *Dockerfile
    rules.append((True, ['*.dockerignore']))
    rules.append((True, ['*Dockerfile']))
    return rules


def dockerignore_to_files(dryrun: bool, dockerignore: str, build_root: str):
    '''Split dockerignore into exclude and include files (format rsync expects).

    This manually tries to compose a list of files matching .dockerignore since
    rsync expects a very different syntax.
    '''
    logger.info('Calculating .dockerignore. This could take a while.')
    with open(dockerignore) as f:
        rules = parse_ignore_rules(f.readlines())
        # Walk all files.
        matches = []
        for root, subdirs, filenames in os.walk(build_root):
            # TODO: might want to include empty directories
            links = [f for f in subdirs if os.path.islink(os.path.join(root, f))]

            for filename in filenames+links:
                path = os.path.normpath(os.path.join(root, filename))
                # Use relative paths
                if path.startswith(build_root):
                    path = path[len(build_root) + 1:]
                if is_included(path, rules):
                    matches.append(path)

        utils.write(dryrun, INCLUDE_PATH, '\n'.join(matches))

def match_path(path: Tuple[str], rule: List[str]):
    '''True if any segment of the path matches the rule.'''
    # Must have recursed a bunch and have a match!
    if not rule:
        return True
    elif rule[0] == '*':
        return True
    # Match against this path anywhere.
    if rule[0] == '**':
        return fnmatch.filter(path, rule[-1])
    # Recurse to follow directory wildcards, or segments match.
    elif rule[0] == '*' or fnmatch.fnmatch(path[0], rule[0]):
        return match_path(path[1:], rule[1:])
    else:
        return False

def is_included(path: str, rules: List[Tuple[bool, List[str]]]):
    '''True if the path passes the rules.
    Apply rules in order.
    The algorithm is based on the description in
    https://docs.docker.com/engine/reference/builder/#dockerignore-file
    '''
    path = path.lstrip('/').split('/')

    ret = True

    for include, rule in rules:
        if match_path(path, rule):
            ret = include
    return ret


def remote_build(dryrun: bool, builder, argv: List[str]):
    build = builder.run(dryrun, return_build_only=True)
    dockerfile = None
    i = None
    try:
        dockerfile, i = build.write_dockerfile_and_dockerignore(dryrun)
        build_root = build.build_root
        root = os.path.abspath(build_root)
        cwd = os.getcwd()
        assert cwd.startswith(root), '--rsync requires that working directory be in build root: root={} cwd={}'.format(root, cwd)

        dockerignore_to_files(dryrun, build.dockerignore, build_root)

        logger.info('Rsync from %s', build_root)
        # Determine remote path
        host = os.getenv('DOCKER_HOST')
        assert host, 'Can\'t rsync with no host. Did you run `docify`?'
        # Strip off extra stuff.
        host = urlparse(host).hostname
        user = os.getenv('OPENAI_USER')
        if build_root[-1] != '/':
            build_root += '/'
        # Install docker-buildtool
        utils.execute_command(dryrun, [
            'ssh', '-t', '{0}@{1}'.format(user, host),
            'bash -l -c "if ! which docker-buildtool; then sudo pip install docker-buildtool; fi; if ! stat /tmp/{0}/docker; then mkdir -p /tmp/{0}/docker; fi"'.format(user)])
        # rsync over the files
        utils.execute_command(dryrun, [
            'rsync', '-avzh', '--files-from={}'.format(INCLUDE_PATH), '--stats', '-e', 'ssh', build_root,
            '{0}@{1}:/tmp/{0}/docker/'.format(user, host)
        ])

        # Execute docker-buildtool remotely.
        argv[0] = 'docker-buildtool'
        argv.remove('--rsync')
        suffix = cwd[len(root):]
        utils.execute_command(dryrun, [
            'ssh', '-t', '{0}@{1}'.format(user, host),
            'bash -l -c "cd /tmp/{}/docker{} && {}"'.format(user, suffix, ' '.join(argv))])

    finally:
        if dockerfile:
            dockerfile.close()
        if i:
            build.restore_dockerignore(dryrun, i)
