#!/usr/bin/env python
"""Stuff related to X keyboard"""
import pprint
import xkbgroup


def main():
    """Main"""
    non_symbols = xkbgroup.XKeyboard.non_symbols.copy()
    non_symbols.add('capslock')
    xkb = xkbgroup.XKeyboard(non_symbols=non_symbols)
    # NOTE: Some of these xkb commands will fail unless my patched version of
    # xkbgroup is used
    layout = xkb.group_data.symbol
    name = xkb.group_data.name
    variant = xkb.group_data.variant
    mdict = {
        'name': name,
        'layout': layout,
        'variant': variant,
    }
    pprint.pprint(mdict)


if __name__ == "__main__":
    main()
