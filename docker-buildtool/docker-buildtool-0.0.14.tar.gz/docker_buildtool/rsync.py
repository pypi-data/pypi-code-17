from urllib.parse import urlparse
import fnmatch
import logging
import os
from typing import List, Tuple, Dict

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

def remote_build(dryrun: bool, build, docker_args: List[str]):
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
        # Determine remote host.
        host = os.getenv('DOCKER_HOST')
        assert host, 'Can\'t rsync with no host. Did you run `docify`?'
        # Strip off extra stuff.
        host = urlparse(host).hostname
        user = os.getenv('OPENAI_USER')
        if build_root[-1] != '/':
            build_root += '/'
        remote_dest = '/tmp/{0}/docker'.format(user)
        remote_temp = '/tmp/{0}/tmp/docker'.format(user)
        # Install docker-buildtool, prep dirs.
        utils.execute_command(dryrun, [
            'ssh', '-t', '{0}@{1}'.format(user, host),
            'bash -l -c "if ! which docker-buildtool; then sudo pip install -U docker-buildtool; fi; if ! stat {0}; then mkdir -p {0}; fi; if ! stat {1}; then mkdir -p {1}; fi; rm -rf {1}"'.format(remote_dest, remote_temp)])
        # rsync the files to remote
        # Delete unwanted ones: http://stackoverflow.com/a/15192150
        utils.execute_command(dryrun, [
            'rsync', '-avzh', '--link-dest={}'.format(remote_dest), '--files-from={}'.format(INCLUDE_PATH), '--stats', '-e', 'ssh', build_root,
            '{0}@{1}:{2}/'.format(user, host, remote_temp)
        ])

        # Move files and execute docker-buildtool remotely.
        suffix = cwd[len(root):]
        command = ['docker-buildtool', '-f', build.dockerfile[len(build_root) + len(suffix):], 'build']
        assert build.docker_repo is not None
        assert build.tag is not None
        command += ['-t', '{}:{}'.format(build.docker_repo, build.tag)]
        for k, v in build.variables.items():
            command += ['-v', '{}={}'.format(k, v)]
        if build.no_fetch:
            command += ['--no-fetch']
        else:
            command += ['--fetch']

        command += ['--'] + docker_args
        # TODO: shellquote?
        command = ' '.join(command)

        utils.execute_command(dryrun, [
            'ssh', '-t', '{0}@{1}'.format(user, host),
            'bash -l -c "rm -r {0}; mv {1} {0}; cd {0}{2} && {3}"'.format(remote_dest, remote_temp, suffix, command)])

    finally:
        if dockerfile:
            dockerfile.close()
        if i:
            build.restore_dockerignore(dryrun, i)
