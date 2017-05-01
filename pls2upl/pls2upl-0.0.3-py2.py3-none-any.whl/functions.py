import hashlib
import json
import os
import uuid
try:
    from ConfigParser import ConfigParser, NoOptionError
except ImportError:
    from configparser import ConfigParser, NoOptionError

import mutagen


def _calculate_checksums(filename):
    """Calculate checksums for a given filename."""
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


def _get_tag_value(tags, keys):
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
    """Look up a track and return a UPL-compatible dict of information."""
    if not os.path.exists(filename):
        # Preserve files we can't find.
        return {
            "artist": "Unknown",
            "title": "Unknown",
            "ids": {"filepath": filename}
        }

    tags = mutagen.File(filename)
    ids = _calculate_checksums(filename)
    ids["filepath"] = filename

    if "TXXX:MusicBrainz Release Track Id" in tags:
        ids["mbtrackid"] = tags["TXXX:MusicBrainz Release Track Id"].text[0]

    if "UFID:http://musicbrainz.org" in tags:
        ids["mbrecid"] = tags["UFID:http://musicbrainz.org"].data.decode("utf8")

    entry_dict = {
        "ids": ids,
        "duration": tags.info.length,
    }

    entry_dict["artist"] = _get_tag_value(tags, ["TPE1", "artist", "aART"])
    entry_dict["title"] = _get_tag_value(tags, ["TIT2", "title", "\xa9nam"])
    entry_dict["album"] = _get_tag_value(tags, ["TALB", "album", "\xa9alb"])

    return entry_dict


def write_upl(entries, outfile):
    """
    Accept a list of dictionaries (as returned by look_up_track) and write them
    into a UPL file.
    """
    data = [{
        "format": "UPL1",
        "name": os.path.basename(outfile),
        "id": str(uuid.uuid4()),
        "entries": entries,
    }]

    with open(outfile, "w") as outf:
        json.dump(data, outf, indent=2, sort_keys=True)
