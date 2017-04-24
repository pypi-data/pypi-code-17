import hashlib
import json
import os
import sys
import uuid
try:
    from ConfigParser import ConfigParser, NoOptionError
except ImportError:
    from configparser import ConfigParser, NoOptionError

import click
import mutagen
try:
    import tbvaccine
    tbvaccine.add_hook()
except:
    pass

try:
    from . import __version__
except (SystemError, ValueError):
    from __init__ import __version__


def calculate_checksums(filename):
    algs = {
        "md5": hashlib.md5(),
        "sha2": hashlib.sha256(),
    }
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            for alg in algs.values():
                alg.update(chunk)
    return {name: alg.hexdigest() for name, alg in algs.items()}


def read_pls(filename):
    """Read a PLS file."""
    config = ConfigParser()
    config.read(filename)
    filenames = []
    for count in range(1, 1 + int(config.get("playlist", "NumberOfEntries"))):
        try:
            item = config.get("playlist", "File%d" % count)
        except NoOptionError:
            continue
        filenames.append(item)
    return filenames


def get_tag_value(tags, keys):
    """
    Retrieve a value from a list of tags in a file.

    The tags will be tried one by one until one is found.
    """
    for tag in keys:
        if tag in tags.keys():
            value = tags[tag][0]
            return value
    return "Unknown"


def look_up_track(filename):
    if not os.path.exists(filename):
        return None

    tags = mutagen.File(filename)
    ids = calculate_checksums(filename)
    ids["filepath"] = filename

    if "TXXX:MusicBrainz Release Track Id" in tags:
        ids["mbtrackid"] = tags["TXXX:MusicBrainz Release Track Id"].text[0]

    if "UFID:http://musicbrainz.org" in tags:
        ids["mbrecid"] = tags["UFID:http://musicbrainz.org"].data.decode("utf8")

    entry_dict = {
        "ids": ids,
        "duration": tags.info.length,
    }

    entry_dict["artist"] = get_tag_value(tags, ["TPE1", "artist", "aART"])
    entry_dict["title"] = get_tag_value(tags, ["TIT2", "title", "\xa9nam"])
    entry_dict["album"] = get_tag_value(tags, ["TALB", "album", "\xa9alb"])

    return entry_dict


def write_upl(filenames, outfile):
    entries = []
    for filename in filenames:
        click.echo("Processing %s..." % filename)
        entry = look_up_track(filename)
        if entry is None:
            entry = {
                "artist": "Unknown",
                "title": "Unknown",
                "ids": {"filepath": filename}
            }
        entries.append(entry)

    data = [{
        "format": "UPL1",
        "name": os.path.basename(outfile),
        "id": str(uuid.uuid4()),
        "entries": entries,
    }]

    with open(outfile, "w", encoding="utf-8") as outf:
        json.dump(data, outf, indent=2, sort_keys=True)


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
        write_upl(filenames, outfile)
    else:
        click.echo("Format not yet supported.")
        sys.exit(1)


if __name__ == "__main__":
    cli()
