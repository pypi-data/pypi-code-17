import logging

import click

from kibitzr.main import main


LOG_LEVEL_CODES = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
}


@click.command()
@click.option("--once", is_flag=True,
              help="Run checks once and exit")
@click.option("-l", "--log-level", default="info",
              type=click.Choice(LOG_LEVEL_CODES.keys()),
              help="Logging level")
@click.argument('name', nargs=-1)
def entry(once, log_level, name):
    """Run kibitzr in the foreground mode"""
    log_level_code = LOG_LEVEL_CODES[log_level]
    main(once=once, log_level=log_level_code, names=name)


if __name__ == "__main__":
    entry()
