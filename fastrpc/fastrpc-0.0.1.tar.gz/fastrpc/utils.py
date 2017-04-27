# -*- coding:utf-8 -*-
import json
import pprint

MSG = '{color}{content}{nc}'

RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"

REVERSE = "\033[;7m"
NC = "\033[0m"

pp = pprint.PrettyPrinter(indent=4)


def alert(content, color=RED):
    return MSG.format(color=color, content=content, nc=NC)


def parse_collection_file(path):
    with open(path) as fp:
        return json.load(fp)
