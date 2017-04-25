#!/usr/bin/env python3

import re
import os
import os.path
import shutil
import functools
import itertools

from collections import namedtuple
from datetime import datetime

import click

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


REGEX_TEMPLATES = {
    'media.ccc.de': (
        '(?P<conference_name>\w+?)'
        '(?P<year>\d{2}(?:\d{2})?)?-'
        '(?P<video_id>\d+)-'
        '(?P<lang>(?:(?:[dD][eE][uU]?|[eE][nN][gG]?|(?:[fF][rR]|[sS][pP])[aA]?|[rR][uU][sS]?|gsw)-)+)'
        '(?P<title>.*?)'
        '(?:_(?P<quality>webm(?:-(h|s)d)?|h264(?:-(?:h(d|q)|iprod))|(h|s)d)|iProd|o(?:pus|gg)|mp3)?'
        '\.(?P<fileext>webm|mp(?:4|3)|o(?:pus|gg))$'
    ),
    'c3l_press': (
        '(?P<date>(?:(?:[12][0-9]|0[1-9])_02|'
        '(?:30|[12][0-9]|0[1-9])_(?:0[469]|11)|'
        '(?:3[01]|[12][0-9]|0[1-9])_(?:0[13578]|1[02]))_'
        '(?:[0-9]{4}))-'
        '(?P<media>\w+)'
        '(?:-(?P<program>\w+))?'
        '(?P<title>.*?)'
        '\.(?P<fileext>p(?:df|ng)|mp(?:3|4))$'
    ),
    'chaosradio': (
        'cr-(?P<episode_number>\d+)-'
        '(?P<lang>deu)-'
        'CR\d+_-_'
        '(?P<title>.*?)'
        '(?:_(?P<quality>webm(?:-(h|s)d)|(h|s)d))'
        '\.(?P<fileext>webm|mp(?:4|3)|o(?:pus|gg))$'
    ),
    'cre.fm': (
        'cre-(?P<episode_number>\d+)-'
        '(?P<title>.*?)'
        '\.(?P<fileext>m(?:4a|p3)|o(?:ga|pus)$'
    ),
    'music': (
        '(?P<albumartist>.*?)/'
        '(?:(?P<year>\d{4})_)?'
        '(?:(?P<month>\d{2})_)?'
        '(?:(?P<day>\d{2})_)?'
        '(?:_-_)?(?P<album>.*?)'
        '(?:_-_(?P<releasecountry>[A-Z]{2})-Release)?/'
        '(?:CD_(?P<discnumber>\d+)/)?'
        '(?P<tracknumber>\d+)_-_(?P<title>.*?)'
        '\.(?P<fileext>mp3|flac|ogg)$'
    ),
    'critical_role': (
        '(?P<title>.*?)(?:_LIVE)?_(?:-_)?Critical_Role_RPG_(?:Show_)?(?:LIVE_)?(?:-_)?'
        'Episode_(?P<episode_number>\d+)-'
        '(?P<video_id>.*?)'
        '\.(?P<fileext>m(?:kv|p4)|webm)$'
    ),
    'gm_tips': (
        '(?P<title>.*?)_'
        'G(?:M|ame_Master)_Tips(?:_w_(?:Matt_Mercer|Satine_Phoenix))?-'
        '(?P<video_id>.*?)'
        '\.(?P<fileext>mkv|webm)$'
    ),
}

output_template = namedtuple('output_template', ['template', 'engine'])

OUTPUT_TEMPLATES = {
    'critical_role': output_template(
        engine='jinja2',
        template=(
            '{{ "{:03d}".format(episode_number|int) }}-{{ title }}.{{ fileext }}'
        )
    ),
    'tv_series': output_template(
        engine='jinja2',
        template=(
            '{{ series_title.replace(" ", "_") }}/'
            '{{ "Season_{:02d}.format(season_number|int) }}'
            '{% if season_title %}-{{ season_title.replace(" ", "_") }}{% endif %}/'
            '{{ "{:02d}".format(episode_number|int) }}-{{ episode_title.replace(" ", "_") }}.{{ fileext }}'
        )
    ),
}


def move_file(old_filename, new_filename, force, abort_on_path_exists, dry_run):

    # Create new directories if needed
    dirs = os.path.dirname(new_filename)
    if dirs:
        os.makedirs(dirs, exist_ok=True)

    if not dry_run:
        if force or not os.path.exists(new_filename):
            shutil.move(old_filename, new_filename)
        else:
            click.secho('{} does exist!'.format(new_filename), fg='red')
            if abort_on_path_exists:
                raise SystemExit


def walk(dir, recursive=False, match_directories=False):
    for entry in os.scandir(dir):
        is_dir = entry.is_dir()
        if recursive and is_dir:
            yield from walk(entry.path)
        elif entry.is_file() or (match_directories and is_dir):
            yield entry
        else:
            continue


def full_path(filename, match_full_path=False):
    return filename.path if match_full_path else filename.name


def apply_regex(walk_function, regex_input_pattern, full_path):
    matches = {}
    has_invalid_matches = False
    for f in walk_function:
        subject = full_path(f)
        match = regex_input_pattern.search(subject)
        if match is None:
            click.secho('{} did not match'.format(subject), fg='red')
            has_invalid_matches = True
        else:
            matches[f] = match

    return matches, has_invalid_matches


@click.command(context_settings={'help_option_names': ('-h', '--help', '-?')})
@click.option('-i', '--interactive', is_flag=True, default=False,
              help='Prompt before renaming files')
@click.option('-d', '--directory', multiple=True, default=['./'])
@click.option('-f', '--force', is_flag=True, default=False,
              help='Force rename')
@click.option('-m', '--match-directories', is_flag=True, default=False,
              help='Search directory name also for matches')
@click.option('-r', '--recursive', is_flag=True, default=False,
              help='Recurse also into subdirectories')
@click.option('-t', '--template-engine', default='python', type=click.Choice(['python', 'jinja2']),
              help='Select template engine to use')
@click.option('-p', '--use-predefined-regex-pattern', is_flag=True, default=False,
              help='Use predefined regex patterns')
@click.option('-o', '--use-predefined-output-template', is_flag=True, default=False,
              help='Use predefined output template')
@click.option('--abort-on-no-match', is_flag=True, default=False,
              help='Exit if a name does not match the INPUT_PATTERN')
@click.option('--abort-on-path-exist', is_flag=True, default=False,
              help='Exit if a renamed path already exists')
@click.option('--match-full-path', is_flag=True, default=False,
              help='Match on full path instead of only filename')
@click.option('-n', '--dry-run', is_flag=True, default=False,
              help='Perform a trial run with no changes made')
@click.version_option()
@click.argument('regex-pattern')
@click.argument('output-pattern')
def pattern_rename(
        regex_pattern,
        output_pattern,
        interactive,
        directory,
        force,
        match_directories,
        recursive,
        template_engine,
        use_predefined_regex_pattern,
        use_predefined_output_template,
        abort_on_no_match,
        abort_on_path_exist,
        match_full_path,
        dry_run,
):
    """Rename files from REGEX_PATTERN to OUTPUT_PATTERN."""

    if use_predefined_output_template:
        try:
            template_tuple = OUTPUT_TEMPLATES[output_pattern]
        except KeyError:
            click.secho('{} does not exists!'.format(output_pattern), fg='red')
            click.echo('Possible predefined patterns:')
            for template_name, template in sorted(OUTPUT_TEMPLATES.items(), key=lambda x: x[1]):
                click.echo('{}, engine={}'.format(template_name, template.engine))
            raise SystemExit
        else:
            template_engine = template_tuple.engine
            output_pattern = template_tuple.template

    if template_engine == 'jinja2':
        if jinja_feature:
            template = jinja_env.from_string(output_pattern)
            output_function = template.render
        else:
            click.secho('jinja2 not installed!', fg='red')
            raise SystemExit
    else:
        output_function = output_pattern.format

    if use_predefined_regex_pattern:
        try:
            regex_pattern = REGEX_TEMPLATES[regex_pattern]
        except KeyError:
            click.secho('{} does not exists!'.format(regex_pattern), fg='red')
            click.echo('Possible predefined patterns:')
            for pattern_name in sorted(REGEX_TEMPLATES):
                click.echo(pattern_name)
            raise SystemExit

    regex_input_pattern = re.compile(regex_pattern)

    walk_function = functools.partial(walk, recursive=recursive, match_directories=match_directories)
    new_walk = itertools.chain.from_iterable(map(walk_function, directory))
    full_path_function = functools.partial(full_path, match_full_path=match_full_path)
    matches, has_invalid_matches = apply_regex(new_walk, regex_input_pattern, full_path_function)

    if has_invalid_matches and abort_on_no_match:
        raise SystemExit

    for f, match in matches.items():
        groupdict = match.groupdict()
        new_filename = output_function(**groupdict)
        click.echo('{} -> {}'.format(f.path, new_filename))
        if not (interactive and not click.confirm('Is the match correct?')):
            move_file(f.path, new_filename, force, abort_on_path_exist, dry_run)


if __name__ == '__main__':
    pattern_rename()
