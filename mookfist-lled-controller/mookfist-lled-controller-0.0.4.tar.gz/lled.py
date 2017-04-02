#!/usr/bin/env python
"""Mookfist LimitlessLED Control

This tool can be used to control your LimitlessLED based lights.

Usage:
    lled.py fade <start> <end> (--group=<GROUP>)... [options]
    lled.py fadec <start> <end> (--group=<GROUP>)... [options]
    lled.py fadeb <startb> <endb> <startc> <endc> (--group=<GROUP>)... [options]
    lled.py color <color> (--group=<GROUP>)... [options]
    lled.py brightness <brightness> (--group=<GROUP>)... [options]

Options:
    -h --host=HOST            IP / Hostname of the bridge
    -p --port=PORT            Port number of the bridge (defaults to 8899)
    -g GROUP --group=GROUP    Group number
    -r RC --repeat=RC         Number of times to repeat a command
    --pause=PAUSE             Number of milliseconds to wait between commands
    -v --version              Specify the bridge version (defaults to 4)
    --debug                   Enable debugging output
    -h --help                 Show this help
"""
import sys
import logging
from docopt import docopt

from mookfist_lled_controller.cli import configure_logger
from mookfist_lled_controller.cli import Main

def main():
    arguments = docopt(__doc__, version='Mookfist LimitlessLED Control 0.0.1')
    configure_logger(arguments['--debug'])

    log = logging.getLogger('lled')

    log.info('Welcome to the Mookfist LimitlessLED Controller')

    try:
        m = Main(arguments)
        m.run()
    except KeyboardInterrupt:
        log.warning('Stopping')


if __name__ == '__main__':
    main()
