#!/usr/bin/python
import sys
from os.path import realpath, join, dirname

source_dir = join(dirname(realpath(__file__)), '..')
print source_dir
sys.path.insert(0, source_dir)
from quickweb import app

if __name__ == "__main__":
    app.run()