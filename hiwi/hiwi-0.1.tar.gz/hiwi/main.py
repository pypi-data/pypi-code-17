#!/usr/bin/python3 
# coding=utf-8

"""Hiwi.

Usage:
  hiwi [OPTIONS] command <arguments>
  hiwi package <name>
  hiwi integrate <zip_filename> 
  hiwi --sfile=session_config.py ...
  hiwi -h | --help
  hiwi --version

Options:
  --sfile=settings.py     Use different settings file [default: settings.py]
  -h --help               Show this screen.
  --version               Show version.

"""
from . import hiwi
from docopt import docopt


def main():
	arguments = docopt(__doc__, version='Hiwi 0.1')
	#print(arguments)
	h = hiwi.Hiwi(arguments["--sfile"][0])
	if arguments["integrate"]:
		h.integrate( arguments["<zip_filename>"] )

	if arguments["package"]:
		h.package( arguments["<name>"] )