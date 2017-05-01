import sys

import click
try:
    import tbvaccine
    tbvaccine.add_hook()
except:
    pass

try:
    from . import __version__
except (SystemError, ValueError):
    from __init__ import __version__

from .functions import read_pls, look_up_track, write_upl


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(
    version=__version__,
    prog_name="pls2upl",
    message="%(prog)s %(version)s: Go forth, and multiply."
)
@click.argument('infile', type=click.Path(exists=True))
@click.argument('outfile', type=click.Path())
def cli(infile, outfile):
    """pls2upl is a command-line utility to convert PLS/M3U/etc playlists to and from UPL."""
    if infile.lower().endswith(".pls"):
        filenames = read_pls(infile)
    else:
        click.echo("Format not yet supported.")
        sys.exit(1)

    entries = []
    for filename in filenames:
        click.echo("Processing %s..." % filename)
        entry = look_up_track(filename)
        entries.append(entry)

    write_upl(entries, outfile)


if __name__ == "__main__":
    cli()
