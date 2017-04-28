#!/usr/bin/env python3

import click  # pip install --user click
import json
import sys
import re
from random import randint
from difflib import SequenceMatcher
import wget  # pip install --user wget
import plumbum  # pip install --user plumbum
from time import sleep
from path import Path  # pip install --user path.py
from libcrap.core import save_json


THIS_DIR = Path(__file__).dirname()

vkfindaudio_w3m = plumbum.local[THIS_DIR.joinpath("vkfindaudio-w3m")]


def string_similarity(s1, s2):
    return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()


def download_track(track, output_dir, min_wait, max_wait, downloaded):
    try:
        script_output = vkfindaudio_w3m(track["artist"]).splitlines()
        title_matches = [line for line in script_output if track["title"].lower() in line.lower()]
        if len(title_matches) == 0:
            print("Didn't find '{0}' - '{1}'. It's possible that vk.com temporarily banned this ip "
                  "or username from audio seach.".format(track["artist"], track["title"]),
                  file=sys.stderr)
        else:
            results = [
                re.match(
                    r"""^(?P<url>http[^\s]+)   # url
                        \s+                    # some spaces after url, greedy match
                        (?P<artist>[^-]*?)     # artist, non-greedy match
                        \s*-\s*                # dash and maybe some spaces around it, greedy match
                        (?P<title>.*?)         # title, non-greedy match because spaces
                        $                      # end of string
                    """,
                    line,
                    flags=re.VERBOSE
                ).groupdict() for line in title_matches
            ]
            similarities = [
                (
                    string_similarity(track["artist"], result["artist"]) +
                    string_similarity(track["title"], result["title"])
                )
                for result in results
            ]
            index_with_max_similarity = max(enumerate(similarities), key=lambda pair: pair[1])[0]
            best_result = results[index_with_max_similarity]
            filename = "{0} - {1}.mp3".format(best_result["artist"], best_result["title"]) \
                .replace("/", "|")  # escape forward slashes coz they are disallowed in filename
            dl_path = output_dir.joinpath(filename)
            wget.download(best_result["url"], dl_path)
            print("\n")
            print("Downloaded '{0}'".format(dl_path))
            downloaded.append(track)
    except plumbum.ProcessExecutionError as e:
        print("Something failed for '{0}' - '{1}'".format(track["artist"], track["title"]))
        print(e, file=sys.stderr)
    sleep_for = randint(min_wait, max_wait)
    print("Sleeping for {0} seconds, otherwise vk.com will punish me".format(sleep_for))
    sleep(sleep_for)


@click.command()
@click.argument("input_json", type=click.File("r", encoding="utf-8"))
@click.argument(
    "output_dir",
    type=click.Path(exists=True, dir_okay=True, file_okay=False, writable=True, readable=False))
@click.option("--min-wait", "-w", type=int, default=50, show_default=True,
              help="wait for at least this many seconds after each search request")
@click.option("--max-wait", "-W", type=int, default=90, show_default=True,
              help="wait for at most this many seconds after each search request")
def main(input_json, output_dir, min_wait, max_wait):
    output_dir = Path(output_dir)
    assert 0 <= min_wait <= max_wait
    tracks = json.load(input_json)
    downloaded = []  # tracks that were successfully downloaded
    try:
        for track in tracks:
            download_track(track, output_dir, min_wait, max_wait, downloaded)
    finally:
        didnt_download = [track for track in tracks if track not in downloaded]
        if didnt_download:
            didnt_dl_log = output_dir.joinpath("failed_to_dl.json")
            save_json(didnt_download, didnt_dl_log)
            print("Listed tracks we didn't dl to {0}".format(didnt_dl_log), file=sys.stderr)


if __name__ == "__main__":
    main()
