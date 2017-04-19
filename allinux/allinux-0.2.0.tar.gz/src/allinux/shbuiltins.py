"""
Bash builtin commands.
"""

import os


def cd(path=None):
    if path:
        os.chdir(path)
    else:
        home_dir = os.environ['HOME']
        os.chdir(home_dir)


def pwd():
    return os.getcwd()
