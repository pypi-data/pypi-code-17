import sys
import logging
from pathlib import Path

import click
from crayons import green, yellow, red, cyan, magenta, white
import blindspin

from . import utils


log = logging.getLogger(__name__)


@click.command()
@click.option('--init', is_flag=True, help="Generate a sample config file.")
@click.option('-v', '--verbose', count=True)
def main(init=False, verbose=0):
    configure_logging(verbose)
    if init:
        do_init()
    else:
        data = do_run()
        do_report(data)


def do_init():
    config, created = utils.init_config()

    if created:
        click.echo(green("Generated config file: ") +
                   white(f"{config.path}", bold=True))
    else:
        click.echo(yellow("Config file already exists: ") +
                   white(f"{config.path}", bold=True))

    click.echo(cyan("Edit this file to match your application"))

    sys.exit(0)


def do_run(config=None):
    config = config or utils.find_config()

    if not config:
        click.echo(red("No config file found"))
        click.echo(cyan("Generate one with the '--init' command"))
        sys.exit(1)

    for sourcefile in config.sourcefiles:
        click.echo(magenta("Loading variables from source file: ") +
                   white(f"{sourcefile.path}", bold=True), err=True)
        sourcefile.fetch()

    for environment in config.environments:
        click.echo(magenta("Loading variables from environment: ") +
                   white(f"{environment.name}", bold=True), err=True)
        with blindspin.spinner():
            environment.fetch()

    rows = utils.generate_table(config)

    return rows


def do_report(rows):
    path = Path.cwd().joinpath("env-diff.md")
    utils.write_markdown(rows, path)
    click.echo(green("Created Markdown report: ") +
               white(f"{path}", bold=True), err=True)


def configure_logging(verbosity=0):
    if verbosity >= 2:
        level = logging.DEBUG
    elif verbosity >= 1:
        level = logging.INFO
    else:
        level = logging.WARNING

    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    logging.getLogger('yorm').setLevel(logging.WARNING)


if __name__ == '__main__':  # pragma: no cover
    main()
