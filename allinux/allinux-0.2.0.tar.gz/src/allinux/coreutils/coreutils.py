"""
https://www.gnu.org/software/coreutils/manual/html_node/index.html
"""

import argparse
from collections import namedtuple
import os
import platform
import shutil



#
# Special file types
#

def mkdir(path, recursive=False, mode=0o777, *, dir_fd=None):
    """
    Mimic 'mkdir' command.
    
    If recursive is True, equal to 'mkdir -p'.
    """

    if recursive:
        os.makedirs(path, mode, exist_ok=True)
    else:
        os.mkdir(path, mode, dir_fd=dir_fd)


def mv(src, dst, copy_function=shutil.copy2):
    shutil.move(src, dst, copy_function=copy_function)


def rm(path):
    os.rmdir(path)


