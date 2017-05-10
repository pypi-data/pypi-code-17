# -*- coding: utf-8 -*-

import sys
import ast

from iftttcml import buildparser


def main():
    """Run the command-line interface."""

    parser = buildparser.build_parser()
    options = parser.parse_args()

    if options.key is None:
        print("Error: Must provide IFTTT secret key.")
        sys.exit(1)

    if options.event:
        params = ast.literal_eval(options.params)

        # cargo dinamicamente el event/event que toca
        ns = {}
        fs = 'from iftttcml.events import {m} as mod'.format(m=options.event)
        exec(fs, globals(), ns)
        mod = ns['mod']

        mod.launch(options.key, options.event, params)


if __name__ == '__main__':
    main()
