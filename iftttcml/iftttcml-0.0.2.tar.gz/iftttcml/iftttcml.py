# -*- coding: utf-8 -*-

import sys
import ast

from iftttcml import buildparser
from iftttcml.makers import metrovlc_sin_saldo


def main():
    """Run the command-line interface."""

    parser = buildparser.build_parser()
    options = parser.parse_args()

    if options.key is None:
        print("Error: Must provide IFTTT secret key.")
        sys.exit(1)

    if options.maker:
        # print('maker!')
        if options.maker == 'metrovlc_sin_saldo':
            params = ast.literal_eval(options.params)
            metrovlc_sin_saldo.launch(options.key, params)


if __name__ == '__main__':
    main()
