# -*- coding: utf-8 -*-

# BSD License
#
# Copyright (c) 2017, Kaffi LLC.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice, this
#   list of conditions and the following disclaimer in the documentation and/or
#   other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.


from pathlib import Path
from pprint import pformat
import sys
import typing

import click
import pathspec
import yaml

from headercop import headercop


# Default config for headercop
CONFIG = {
    'headercop': {
        'enforced_extensions': [],
        'license': 'bsd3',
        'license_templates': Path(Path(__file__).parent, 'licenses'),
    },
    'enforcers': {
        'py': {
            'perline_prefix': '# ',
            'postfix': '\n\n',
            'skip_lines': 2,  # Max number of lines to skip before header is expected
            'may_skip_regex': '^(#|\s*$)'  # Only lines with this prefix may be skipped before header is expected
        },
        'tf': {
            'perline_prefix': '# ',
            'postfix': '\n\n',
            'skip_lines': 2,  # Max number of lines to skip before header is expected
            'may_skip_regex': '^(#|\s*$)'  # Only lines with this prefix may be skipped before header is expected
        },
    },
    'private': {
        '__config': None,
    },
}


VERBOSE = 0


CONTEXT_SETTINGS = {'help_option_names': ['-h', '--help']}


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-c', '--config', 'config_file', help="config file to use (default headercop.yaml)",
    default=None, type=click.Path(resolve_path=True))
@click.option('-v', '--verbose', count=True, help='Verbosity. Can be specified multiple times')
def cmd(config_file, verbose):
    '''Enforce file headers for a project

    Go through a project and for selected / configured file types enforce a
    particular header. Respects .gitignore

    CONFIG:

    Headercop is configured with a yaml file (headercop.yaml) broken into two
    sections. One for configuring headercop, and another for configuring how
    replacements are done in a file.

    CONFIG FILE EXAMPLE:

    \b
    headercop:
        author: "Author / Company Name"
        program: "Program name"
        license: bsd  # Select the license header you want to enforce
        enforced_extensions:  # Support for these filetypes is built in
            - py  # Python
            - tf  # Terraform
    enforcers:  # Configure substition options for new filetypes, or override defaults
        py:  # e.g. the file extension to search for
            prefix: '#'  # Like "/*" in C++ style comments
            perline_prefix: ''  # Like "#" in most shell languages
            postfix: '#'  # Like "*/" in C++ style comments
            may_skip_regex: '.*'  # See MAYSKIP section

    MAYSKIP:

    Regex for if skipping a line is appropriate. For example in Python, it's
    probably a good idea to skip the "#!/usr/bin/env python" line, but you
    would want to insert the license before any "import" lines.


    '''

    global CONFIG, VERBOSE
    VERBOSE = verbose

    if config_file is None:
        scan_for_config(Path('headercop.yaml'))
    else:  # Direct path to config was given
        config_file = Path(config_file)
        CONFIG['private']['__config'] = config_file
        if not config_file.exists():
            error('Config file "{}" does not exist'.format(config_file))
            sys.exit(1)
        load_config(CONFIG, config_file)
    debug(CONFIG)


@cmd.command()
def supported():
    '''List supported filetypes

    This includes supported types added via additional_templates in the config
    '''

    global CONFIG
    log('Supported filetypes', 'white', '\n{}'.format('\n'.join(CONFIG['enforcers'].keys())))
    log('Enforced filetypes', 'white', '\n{}'.format('\n'.join(CONFIG['headercop']['enforced_extensions'])))


@cmd.command()
@click.argument('PATHS', nargs=-1, required=True, type=click.Path())
def check(paths):
    '''Are files missing a license header

    Check either individual files or paths recursively for the license header
    and report the list of files that need a license header added. If any files
    are missing the header exits with exit code 1. Otherwise will exit normally
    (0)
    '''

    paths = get_paths(paths)
    license = get_license()
    debug('Will apply to')
    debug(paths, indent=2)

    need_license = False
    for path in paths:
        config = CONFIG['enforcers'][path.suffix.lstrip('.')]
        rendered_license = headercop.format_license(
            orignal_text=license,
            prefix=config.get('prefix', ''),
            perline_prefix=config.get('perline_prefix', ''),
            postfix=config.get('postfix', ''))
        with path.open() as f_in:
            # Goofy looking, but the first file that says it needs a license
            # means this stays True for the rest of the run
            has_license = headercop.check_file(f_in, rendered_license, config['skip_lines'] * 2)
            if not has_license:
                log('Missing license header', 'white', str(path))
            need_license = not has_license or need_license
    if need_license:
        sys.exit(1)


@cmd.command()
@click.argument('PATHS', nargs=-1, required=True, type=click.Path())
def inject(paths):
    '''Inject the header (if needed) into supported files on PATHS

    Will apply to all files in PATH recursively if PATH is a directory
    '''

    paths = get_paths(paths)
    license = get_license()
    debug('Will apply to')
    debug(paths, indent=2)

    for path in paths:
        config = CONFIG['enforcers'][path.suffix.lstrip('.')]
        rendered_license = headercop.format_license(
            orignal_text=license,
            prefix=config.get('prefix', ''),
            perline_prefix=config.get('perline_prefix', ''),
            postfix=config.get('postfix', ''))
        with path.open() as f_in:
            has_license = headercop.check_file(f_in, rendered_license, config['skip_lines'] * 2)
        if not has_license:
            info('Adding header to {}'.format(path))
            headercop.inject_header(path, rendered_license, config['skip_lines'], config['may_skip_regex'])


# CLI Utility functions
def debug(msg, indent=0):
    if VERBOSE > 1:
        log('DEBUG', 'cyan', msg, indent)


def error(msg, indent=0):
    log('ERROR', 'red', msg, indent)


def info(msg, indent=0):
    if VERBOSE > 0:
        log('INFO', 'green', msg, indent)


def get_license() -> str:
    license_path = Path(CONFIG['headercop']['license_templates'], '{}.txt'.format(CONFIG['headercop']['license']))
    with license_path.open() as f_in:
        return headercop.render_license(f_in.read(),
            author=CONFIG['headercop']['author'],
            program=CONFIG['headercop']['program'])


def get_paths(paths: typing.Sequence[Path]) -> typing.List[Path]:
    '''Return the set of files headercop should affect
    '''

    gitignore = Path(CONFIG['private']['__config'].parent, '.gitignore')
    gitignored = ['.git']
    if gitignore.exists():
        with gitignore.open() as gitignore_fh:
            gitignored.extend(gitignore_fh)
    ignore_spec = pathspec.PathSpec.from_lines('gitwildmatch', gitignored)
    include_spec = pathspec.PathSpec.from_lines('gitwildmatch',
        ['*.{}'.format(extension) for extension in CONFIG['headercop']['enforced_extensions']])

    paths = [Path(path) for path in paths]
    applicable_paths = []
    for path in paths:
        if path.is_dir():
            applicable_paths.extend([
                subpath for subpath in path.glob('**/*')
                if subpath.is_file()
                and not ignore_spec.match_file(str(subpath))
                and include_spec.match_file(str(subpath))
            ])
        elif path.is_file() \
                and not ignore_spec.match_file(str(path)) \
                and include_spec.match_file(str(path)):
            applicable_paths.append(path)
    return applicable_paths


def log(level, color, msg, indent=0):
    if not isinstance(msg, str):
        # Add indent to each line from pformat except the first line
        msg = ['{}{}'.format(' ' * indent, line)
               for line in pformat(msg).split('\n')]
        msg[0] = msg[0][indent:]
        msg = '\n'.join(msg)
    click.echo(
        (' ' * indent) +
        click.style(level, fg=color, bold=True) +
        click.style(': ', bold=True) +
        msg
    )


def load_config(config, path):
    with path.open() as config_fh:
        loaded_config = yaml.safe_load(config_fh)
    if not loaded_config:  # Empty config means we're good!
        debug('no config settings in {}'.format(path))
        return

    keys = list(k for k in CONFIG.keys() if k not in ('private', 'additional_templates'))
    debug('original config settings before loading')
    debug(config)
    for k in keys:
        config[k].update(loaded_config.get(k, {}))
    debug('updated config settings after loading')
    debug(config)


def scan_for_config(config_file: Path):
    config_file = config_file.absolute()
    while config_file.parent.parent != config_file.parent:  # Go till we hit the root dir
        if config_file.exists():
            info('loading config at {}'.format(config_file))
            load_config(CONFIG, config_file)
            CONFIG['private']['__config'] = config_file
            break
        config_file = Path(config_file.parent.parent, config_file.name)
    else:  # Meaning we didn't break out thus, hit the root dir
        error('No config file found. Either supply -c or CWD should have a headercop.yaml')
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    cmd()
