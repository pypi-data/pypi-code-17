import logging

import click

from eelifx.config import display_config, setup_loop, setup_queryship


def _call_loop(
    mode: str,
    endpoint: str=None,
    config=None,
    loglevel=None,
):
    if loglevel is None:
        loglevel = logging.INFO
    else:
        loglevel = getattr(logging, loglevel)

    setup_loop(
        mode,
        config=config,
        endpoint=endpoint,
        loglevel=loglevel
    )


@click.option(
    '--loglevel',
    default=None,
    help='E.g. "DEBUG" or "INFO"',
)
@click.group()
def root(loglevel=None):
    ''' EELifx Copyright (C) 2017 Chris Speck'''
    pass


@click.command(help='Print default config to standard out.')
def showconfig(loglevel=None):
    display_config()


@click.option(
    '--config',
    default=None,
    type=click.File('rt'),
    help='Path to optional config file with rules to load'
)
@click.command(
    short_help='Execute each rule in succession.',
    help='A test cycle which exercises each rule for each group in succession, resetting lights to base prior to each test.'
)
def grouptest(config=None, loglevel=None):
    _call_loop(
        'grouptest',
        endpoint=None,
        config=config,
        loglevel=loglevel
    )


@click.option(
    '--config',
    default=None,
    type=click.File('rt'),
    help='Path to optional config file with rules to load'
)
@click.argument(
    'endpoint'
)
@click.command(help='Poll and set lights according to game state.')
def run(endpoint, config=None, loglevel=None):
    _call_loop(
        'run',
        endpoint=endpoint,
        config=config,
        loglevel=loglevel
    )


@click.argument(
    'endpoint'
)
@click.option('hull', '-h', type=click.IntRange(0, 2000), help='Set hull level', metavar='<int>')
@click.option('energy', '-e', type=click.IntRange(0, 5000), help='Set energy level', metavar='<int>')
@click.command(short_help='Query EE and set parameters if given.')
def queryship(endpoint, loglevel=None, hull=None, energy=None):
    setup_queryship(endpoint, hull=hull, energy=energy, loglevel=loglevel)


@click.option(
    '--config',
    default=None,
    type=click.File('rt'),
    help='Path to optional config file with rules to load'
)
@click.command(help='Reset lights to base state.')
def reset(config=None, loglevel=None):
    _call_loop(
        'reset',
        endpoint=None,
        config=config,
        loglevel=loglevel
    )


root.add_command(showconfig)
root.add_command(grouptest)
root.add_command(run)
root.add_command(reset)
root.add_command(queryship)

if __name__ == '__main__':
    root()
