"""
Opens a random top-100 YTMND page
"""

import argparse
import os
import random
import time

from pytmnd import ytmnd


DESCRIPTION = "Opens a random top-100 YTMND page.  Control-C to quit."


def open_url(url):
    os.system(f"open {url}")


def parse_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    return parser.parse_args()


def offer_site(site):
    (url, title) = site

    if input(f"[ ] Open '{title}'? (y/n) ") == 'y':
        print(f"    [+] Loading YTMND...\n")
        time.sleep(0.25)
        open_url(url)
        time.sleep(0.25)


def loop(sites):
    while True:
        site = random.choice(sites)
        offer_site(site)


def main():
    _ = parse_args()

    sites = ytmnd.fetch_top_sites()
    try:
        loop(sites)
    except KeyboardInterrupt:
        print("\nYou're the man now, dog!")


if __name__ == '__main__':
    main()
