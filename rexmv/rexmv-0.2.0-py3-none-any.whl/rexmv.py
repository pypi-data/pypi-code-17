#!/usr/bin/env python3

import re
import os
import os.path
import shutil
import functools
import itertools

from datetime import datetime
from typing import (
    Tuple,
    Dict,
    Match,
    Generator,
    List,
    Callable,
    Pattern,
    Iterator,
    Any,
)

import click

CONFIG_PATH = click.get_app_dir('rexmv')

TEMPLATES_PATH = os.path.join(CONFIG_PATH, 'templates')
os.makedirs(TEMPLATES_PATH, exist_ok=True)

REGEX_PATH = os.path.join(CONFIG_PATH, 'regex')
os.makedirs(REGEX_PATH, exist_ok=True)

try:
    import jinja2
except ImportError:
    jinja_feature = False
else:
    jinja_feature = True
    jinja_env = jinja2.Environment()

    def to_datetime(value, format='%Y-%m-%d'):
        return datetime.strptime(value, format)

    def format_datetime(value, format='%Y-%m-%d'):
        return value.strftime(format)

    def to_int(value):
        return int(value)

    def to_float(value):
        return float(value)

    jinja_env.filters['datetime'] = to_datetime
    jinja_env.filters['datetimeformat'] = format_datetime
    jinja_env.filters['int'] = to_int
    jinja_env.filters['float'] = to_float


def move_file(old_filename: str, new_filename: str) -> None:
    # Create new directories if needed
    dirs = os.path.dirname(new_filename)
    if dirs:
        os.makedirs(dirs, exist_ok=True)

    shutil.move(old_filename, new_filename)


def walk(dir: str, recursive: bool=False, match_directories: bool=False) -> Generator[os.DirEntry, None, None]:
    for entry in os.scandir(dir):
        is_dir = entry.is_dir()
        if recursive and is_dir:
            yield from walk(entry.path, recursive, match_directories)
        elif entry.is_file() or (match_directories and is_dir):
            yield entry
        else:
            continue


def full_path(filename: os.DirEntry, match_full_path: bool=False) -> str:
    return filename.path if match_full_path else filename.name


def apply_regex(
        walk_function: Iterator[Any],
        regex_pattern: Pattern,
        full_path: str
) -> Tuple[Dict[os.DirEntry, Match], bool]:
    matches = {}
    has_invalid_matches = False
    for f in walk_function:
        subject = full_path(f)
        match = regex_pattern.search(subject)
        if match is None:
            click.secho('{} did not match'.format(subject), fg='red')
            has_invalid_matches = True
        else:
            matches[f] = match

    return matches, has_invalid_matches


def load_template(template_name: str) -> Tuple[str, str]:
    try:
        with open(os.path.join(TEMPLATES_PATH, template_name), encoding='utf-8') as f:
            template_lines = f.readlines()
    except FileNotFoundError:
        raise
    else:
        lines_length = len(template_lines)
        if lines_length >= 3:
            template_engine = template_lines[0]
            output_pattern = ''.join(template_lines[1:])
        elif lines_length == 2:
            template_engine, output_pattern = template_lines
        else:
            template_engine = 'python'
            output_pattern = template_lines[0]
    return template_engine, output_pattern


def load_regex(regex_name: str) -> str:
    try:
        with open(os.path.join(REGEX_PATH, regex_name), encoding='utf-8') as f:
            return f.read().replace('\n', '')
    except FileNotFoundError:
        raise


@click.command(context_settings={'help_option_names': ('-h', '--help', '-?')})
@click.option('-i', '--interactive', is_flag=True, default=False,
              help='prompt before renaming files')
@click.option('-d', '--directory', multiple=True, default=['./'])
@click.option('-f', '--force', is_flag=True, default=False,
              help='force rename')
@click.option('-m', '--match-directories', is_flag=True, default=False,
              help='search directory name also for matches')
@click.option('-r', '--recursive', is_flag=True, default=False,
              help='search directories recursively')
@click.option('-t', '--template-engine', default='python', type=click.Choice(['python', 'jinja2']),
              help='select the template engine to use')
@click.option('-p', '--use-predefined-regex-pattern', is_flag=True, default=False,
              help='use predefined regex patterns')
@click.option('-o', '--use-predefined-output-template', is_flag=True, default=False,
              help='use predefined output template')
@click.option('--abort-on-no-match', is_flag=True, default=False,
              help='exit if a name does not match the INPUT_PATTERN')
@click.option('--abort-on-path-exist', is_flag=True, default=False,
              help='exit if a renamed path already exists')
@click.option('--match-full-path', is_flag=True, default=False,
              help='match on full path instead of only filename')
@click.option('-n', '--dry-run', is_flag=True, default=False,
              help='perform a trial run with no changes made')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='explain what is being done')
@click.version_option()
@click.argument('regex-pattern')
@click.argument('output-pattern')
def pattern_rename(
        regex_pattern: str,
        output_pattern: str,
        interactive: bool,
        directory: List[str],
        force: bool,
        match_directories: bool,
        recursive: bool,
        template_engine: str,
        use_predefined_regex_pattern: bool,
        use_predefined_output_template: bool,
        abort_on_no_match: bool,
        abort_on_path_exist: bool,
        match_full_path: bool,
        dry_run: bool,
        verbose: bool,
) -> None:
    """Rename files from REGEX_PATTERN to OUTPUT_PATTERN."""

    if use_predefined_output_template:
        try:
            template_engine, output_pattern = load_template(output_pattern)
        except FileNotFoundError:
            click.secho('{} does not exists!'.format(output_pattern), fg='red')
            click.echo('Possible template names:')
            for f in os.listdir(TEMPLATES_PATH):
                click.echo(f)
            raise SystemExit

    if template_engine == 'jinja2':
        if jinja_feature:
            template = jinja_env.from_string(output_pattern)
            render_function = template.render
        else:
            click.secho('jinja2 not installed!', fg='red')
            raise SystemExit
    else:
        render_function = output_pattern.format

    if use_predefined_regex_pattern:
        try:
            regex_pattern = load_regex(regex_pattern)
        except FileNotFoundError:
            click.secho('{} does not exists!'.format(regex_pattern), fg='red')
            click.echo('Possible regex names:')
            for f in os.listdir(REGEX_PATH):
                click.echo(f)
            raise SystemExit

    try:
        regex_pattern_c = re.compile(regex_pattern)
    except re.error as e:
        if verbose:
            click.secho('Regular expression could not be compiled!', fg='red')
        click.secho(e.msg, fg='red')
        raise SystemExit

    # Monkey patch walk function to include commandline options
    walk_function = functools.partial(walk, recursive=recursive, match_directories=match_directories)
    new_walk = itertools.chain.from_iterable(map(walk_function, directory))

    # Monkey patch full_path function to include commandline options
    full_path_function = functools.partial(full_path, match_full_path=match_full_path)

    matches, has_invalid_matches = apply_regex(new_walk, regex_pattern_c, full_path_function)

    if has_invalid_matches and abort_on_no_match:
        raise SystemExit

    new_filenames = dict((f.path, render_function(**match.groupdict())) for f, match in matches.items())

    has_existing = False
    non_existing = {}
    for old, new in new_filenames.items():
        if os.path.exists(new):
            click.secho('{} does exist!'.format(new), fg='red')
            has_existing = True
        else:
            non_existing[old] = new

    if has_existing and abort_on_path_exist:
        raise SystemExit

    if force:
        files_to_move = new_filenames.items()
    else:
        files_to_move = non_existing.items()

    for old, new in files_to_move:
        if verbose or interactive:
            click.echo('{} -> {}'.format(old, new))

        if not (interactive and not click.confirm('Is the match correct?')):
            if not dry_run:
                move_file(old, new)


@click.group(context_settings={'help_option_names': ('-h', '--help', '-?')})
def manage():
    pass


@manage.group()
def template():
    pass


@template.command(name='add')
@click.argument('name')
def template_add(name):
    click.edit(filename=os.path.join(TEMPLATES_PATH, name))


@template.command(name='list')
def template_list():
    for f in os.listdir(TEMPLATES_PATH):
        click.echo(f)


@template.command(name='view')
@click.argument('name')
def template_view(name):
    try:
        with open(os.path.join(TEMPLATES_PATH, name), encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        click.secho('File not found!', fg='red')
        raise SystemExit
    else:
        click.echo_via_pager(text)


@template.command(name='remove')
@click.argument('name')
def template_remove(name):
    try:
        os.remove(os.path.join(TEMPLATES_PATH, name))
    except FileNotFoundError:
        click.secho('Cannot remove {}. It doesn\'t exist!'.format(name))
        raise SystemExit


@manage.group()
def regex():
    pass


@regex.command(name='add')
@click.argument('name')
def regex_add(name):
    click.edit(filename=os.path.join(REGEX_PATH, name))


@regex.command(name='list')
def regex_list():
    for f in os.listdir(REGEX_PATH):
        click.echo(f)


@regex.command(name='view')
@click.argument('name')
def regex_view(name):
    try:
        with open(os.path.join(REGEX_PATH, name), encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        click.secho('File not found!', fg='red')
        raise SystemExit
    else:
        click.echo_via_pager(text)


@regex.command(name='remove')
@click.argument('name')
def regex_remove(name):
    try:
        os.remove(os.path.join(REGEX_PATH, name))
    except FileNotFoundError:
        click.secho('Cannot remove {}. It doesn\'t exist!'.format(name))
        raise SystemExit


if __name__ == '__main__':
    pattern_rename()
